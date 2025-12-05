# app/services/orden_compra_service.py
from sqlalchemy.orm import Session
from app.repositories.orden_compra_repository import OrdenCompraRepository
from app.repositories.inventario_repository import InventarioRepository
from app.repositories.rq_item_repository import RQItemRepository
from app.models.orden_compra_model import OrdenCompraParcial
from app.models.inventario_model import Inventario
from app.services.rq_service import RQService
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.repositories.rq_repository import RQRepository


class OrdenCompraService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = OrdenCompraRepository(db)
        self.inventario_repo = InventarioRepository(db)
        self.rq_item_repo = RQItemRepository(db)

    def _total_comprado_existente(self, rq_item_id: int) -> int:
        ordenes = self.repo.get_by_item(rq_item_id)
        return sum([o.cantidad_comprada or 0 for o in ordenes]) if ordenes else 0

    def create_orden(self, orden_data: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Validaciones básicas y obtención de item
        rq_item = self.rq_item_repo.get_by_id(orden_data["rq_item_id"])
        if not rq_item:
            raise ValueError("El RQItem indicado no existe")

        cantidad_pedida = rq_item.cantidad or 0
        comprado_antes = self._total_comprado_existente(rq_item.id)
        cantidad_nueva = orden_data.get("cantidad_comprada", 0)

        if cantidad_nueva <= 0:
            raise ValueError("La cantidad comprada debe ser mayor que 0")

        # 2. Crear la orden parcial (si quieres guardar sólo cuando estado == 'comprado'
        # se puede condicionar aquí; por ahora guardamos siempre)
        orden = OrdenCompraParcial(**orden_data)
        self.repo.create(orden)

        # 3. Totales y exceso
        total_comprado = comprado_antes + cantidad_nueva
        avance_real_rq = min(total_comprado, cantidad_pedida)
        exceso = max(0, total_comprado - cantidad_pedida)

        progreso_item = round((avance_real_rq / cantidad_pedida) * 100, 2) if cantidad_pedida > 0 else 0
        if avance_real_rq >= cantidad_pedida:
            estado_item = "completado"
        elif avance_real_rq > 0:
            estado_item = "parcial"
        else:
            estado_item = "sin_iniciar"

        # 4. Actualizar inventario (siempre sumar toda la cantidad comprada)
        inventario_item = self.inventario_repo.get_by_codigo(rq_item.codigo)
        if inventario_item:
            nuevo_stock = (inventario_item.cantidad_disponible or 0) + cantidad_nueva
            self.inventario_repo.update_cantidad(inventario_item.id, nuevo_stock)
        else:
            inventario_item = Inventario(
                codigo=rq_item.codigo,
                descripcion=rq_item.descripcion,
                cantidad_disponible=cantidad_nueva,
                ubicacion=orden_data.get("ubicacion_envio", ""),
                rq_item_id=rq_item.id
            )
            self.inventario_repo.create(inventario_item)

        # 5. Recalcular estado del RQ
        rq_actualizado = RQService(self.db).actualizar_estado_compra(rq_item.rq_id)

        # 6. Construir respuesta tipo resumen (para frontend)
        response = {
            "message": "Compra registrada correctamente",
            "orden": orden,  # objecto de SQLAlchemy (router/schema lo convertirá con from_attributes)
            "avance_item": {
                "item_id": rq_item.id,
                "codigo": rq_item.codigo,
                "descripcion": rq_item.descripcion,
                "cantidad_requerida": cantidad_pedida,
                "comprado_antes": comprado_antes,
                "comprado_nuevo": cantidad_nueva,
                "comprado_total": total_comprado,
                "avance_efectivo_rq": avance_real_rq,
                "exceso": exceso,
                "progreso": f"{progreso_item}%",
                "estado_item": estado_item
            },
            "estado_rq": {
                "rq_id": rq_actualizado.id,
                "estado_compra": rq_actualizado.estado_compra,
                "progreso_compra": rq_actualizado.progreso_compra
            }
        }

        return response

    def get_ordenes_by_item(self, rq_item_id: int):
        return self.repo.get_by_item(rq_item_id)
    
    def patch_orden(self, orden_id: int, cambios: Dict[str, Any]):
        """
        Edita parcialmente una orden de compra.
        Ajusta inventario si se modifica la cantidad.
        Valida sobrecupo y devuelve warning si se sobrepasa el RQ.
        """

        orden = self.repo.get_by_id(orden_id)
        if not orden:
            raise ValueError("Orden no encontrada")

        # Obtener item del RQ
        rq_item = self.rq_item_repo.get_by_id(orden.rq_item_id)
        cantidad_pedida = rq_item.cantidad or 0

        # Guardamos la cantidad anterior para ajustar inventario
        cantidad_vieja = orden.cantidad_comprada or 0
        cantidad_nueva = cambios.get("cantidad_comprada", cantidad_vieja)

        # Actualizar inventario solo si cambia cantidad
        if cantidad_nueva != cantidad_vieja:
            diferencia = cantidad_nueva - cantidad_vieja
            inventario_item = self.inventario_repo.get_by_codigo(rq_item.codigo)
            if inventario_item:
                inventario_item.cantidad_disponible += diferencia
                self.inventario_repo.update_cantidad(inventario_item.id, inventario_item.cantidad_disponible)
            else:
                # si no existía inventario, crear con la diferencia
                inventario_item = Inventario(
                    codigo=rq_item.codigo,
                    descripcion=rq_item.descripcion,
                    cantidad_disponible=diferencia,
                    ubicacion=cambios.get("ubicacion_envio", ""),
                    rq_item_id=rq_item.id
                )
                self.inventario_repo.create(inventario_item)

        # Actualizar orden con los cambios
        orden_actualizada = self.repo.update(orden_id, **cambios)

        # Recalcular estado del RQ
        total_comprado = self._total_comprado_existente(rq_item.id)
        exceso = max(0, total_comprado - cantidad_pedida)
        RQService(self.db).actualizar_estado_compra(rq_item.rq_id)

        response = {
            "orden": orden_actualizada,
            "exceso": exceso,
            "warning": f"Se ha sobrepasado la cantidad solicitada por {exceso} unidades" if exceso > 0 else None
        }
        return response


    def update_orden(self, orden_id: int, **kwargs):
        orden = self.repo.update(orden_id, **kwargs)
        if not orden:
            raise ValueError("Orden no encontrada")
        # recalcular estado del RQ asociado
        try:
            rq_item = self.rq_item_repo.get_by_id(orden.rq_item_id)
            RQService(self.db).actualizar_estado_compra(rq_item.rq_id)
        except Exception:
            pass
        return orden

    def delete_orden(self, orden_id: int):
        orden = self.repo.get_by_id(orden_id)
        if not orden:
            raise ValueError("Orden no encontrada")
        rq_item_id = orden.rq_item_id
        self.repo.delete(orden_id)
        try:
            rq_item = self.rq_item_repo.get_by_id(rq_item_id)
            RQService(self.db).actualizar_estado_compra(rq_item.rq_id)
        except Exception:
            pass
        return {"detail": "Orden eliminada"}
    
   
    def listar_ordenes_por_rq(
        self,
        estado: Optional[str] = None,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Devuelve todas las órdenes de compra agrupadas por RQ.
        Incluye progreso numérico para dashboard y porcentaje para visualización.
        Permite filtrar por estado de RQ y rango de fechas.
        """

        rq_repo = RQRepository(self.db)
        rq_list = rq_repo.get_all()

        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d").date() if fecha_inicio else None
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").date() if fecha_fin else None

        resultado = []

        for rq in rq_list:
            fecha_rq = getattr(rq, "fecha_emision", None)

            # Filtrar por rango de fechas
            if fecha_inicio_dt and fecha_rq and fecha_rq < fecha_inicio_dt:
                continue
            if fecha_fin_dt and fecha_rq and fecha_rq > fecha_fin_dt:
                continue

            rq_items = self.rq_item_repo.get_by_rq(rq.id)
            items_con_ordenes = []

            for item in rq_items:
                ordenes = self.repo.get_by_item(item.id)
                comprado_total = sum([o.cantidad_comprada or 0 for o in ordenes])
                cantidad_requerida = item.cantidad or 0
                avance_real_rq = min(comprado_total, cantidad_requerida)
                exceso = max(0, comprado_total - cantidad_requerida)
                progreso_item_num = round((avance_real_rq / cantidad_requerida) * 100, 2) if cantidad_requerida > 0 else 0
                progreso_item = f"{progreso_item_num}%"

                if avance_real_rq >= cantidad_requerida:
                    estado_item = "completado"
                elif avance_real_rq > 0:
                    estado_item = "parcial"
                else:
                    estado_item = "sin_iniciar"

                items_con_ordenes.append({
                    "item_id": item.id,
                    "codigo": item.codigo,
                    "descripcion": item.descripcion,
                    "cantidad_requerida": cantidad_requerida,
                    "unidad": item.unidad,
                    "estado_item": estado_item,
                    "comprado_total": comprado_total,
                    "avance_efectivo_rq": avance_real_rq,
                    "exceso": exceso,
                    "progreso": progreso_item,
                    "progreso_item_num": progreso_item_num,  # nuevo campo
                    "ordenes_parciales": [
                        {
                            "orden_id": o.id,
                            "cantidad_comprada": o.cantidad_comprada,
                            "estado": o.estado,
                            "proveedor": o.proveedor,
                            "tipo_compra": o.tipo_compra,
                            "fecha": o.fecha,
                            "comprobante": o.comprobante,
                            "guia_remision": o.guia_remision,
                            "notas": o.notas
                        } for o in ordenes
                    ]
                })

            # calcular progreso general del RQ limitado al 100%
            total_avance = sum([min(sum([o.cantidad_comprada or 0 for o in self.repo.get_by_item(i.id)]), i.cantidad or 0) 
                                for i in rq_items])
            total_requerido = sum([i.cantidad or 0 for i in rq_items])
            progreso_rq_num = round((total_avance / total_requerido) * 100, 2) if total_requerido > 0 else 0
            if progreso_rq_num > 100:
                progreso_rq_num = 100
            progreso_rq = f"{progreso_rq_num}%"  # formato string

            # determinar estado general del RQ
            estado_rq_calc = (
                "completado" if all([i["estado_item"] == "completado" for i in items_con_ordenes])
                else "no_iniciado" if all([i["estado_item"] == "sin_iniciar" for i in items_con_ordenes])
                else "parcial"
            )

            # filtrar por estado si se indicó
            if estado and estado_rq_calc != estado:
                continue

            resultado.append({
                "rq_id": rq.id,
                "codigo_rq": getattr(rq, "codigo", None),
                "fecha_emision": fecha_rq,
                "estado_rq": estado_rq_calc,
                "progreso_rq": progreso_rq,
                "progreso_rq_num": progreso_rq_num,  # nuevo campo
                "items": items_con_ordenes
            })

        return resultado
