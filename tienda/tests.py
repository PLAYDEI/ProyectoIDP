# Importa la excepción general de Transbank para capturar errores durante el proceso de pago
from transbank.error.transbank_error import TransbankError
# Para devolver respuestas JSON al frontend
from django.http import JsonResponse
# Decorador que permite saltar la validación CSRF (útil en APIs)
from django.views.decorators.csrf import csrf_exempt
# Clase para iniciar una transacción Webpay Plus
from transbank.webpay.webpay_plus.transaction import Transaction
# Configuración de las credenciales para Webpay
from transbank.common.options import WebpayOptions
# Tipo de ambiente (TEST o LIVE)
from transbank.common.integration_type import IntegrationType
# Renderizado de templates
from django.shortcuts import render
import json


# Vista que inicia el proceso de pago
@csrf_exempt
def iniciar_pago(request):
    if request.method == "POST":
        datos = json.loads(request.body)  # Decodifica el JSON recibido
        productos = datos.get("productos", [])  # Obtiene la lista de productos

        if not productos:
            return JsonResponse({"error": "No se seleccionaron productos."}, status=400)

        try:
            # Suma los precios convertidos a float y redondeados
            total = sum(round(float(p["precio"])) for p in productos)
        except (ValueError, KeyError, TypeError) as e:
            return JsonResponse({"error": f"Precio inválido: {str(e)}"}, status=400)

        # Genera valores requeridos por Webpay
        buy_order = f"orden{request.META['REMOTE_ADDR'].replace('.', '')}"
        session_id = "session123"
        return_url = "http://127.0.0.1:8000/pago_exitoso/"  # Donde se redirige tras pagar

        # Credenciales de prueba (Transbank)
        options = WebpayOptions(
            commerce_code="597055555532",
            api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
            integration_type=IntegrationType.TEST
        )

        transaction = Transaction(options)

        try:
            # Crea la transacción
            response = transaction.create(buy_order, session_id, total, return_url)
            return JsonResponse({
                "url_webpay": response['url'] + "?token_ws=" + response['token'],
                "token": response['token']
            })
        except TransbankError as e:
            print("❌ Error en la creación del pago:", e.message)
            return JsonResponse({"error": e.message}, status=500)

    # Si no es POST, rechaza la solicitud
    return JsonResponse({"error": "Método no permitido"}, status=405)


# Vista para mostrar mensaje de éxito (o comprobante)
def pago_exitoso(request):
    token_ws = request.GET.get("token_ws")
    return render(request, "pago_exitoso.html", {"token": token_ws})


# -------------------------- TESTS --------------------------
from django.test import TestCase, Client
from django.urls import reverse

class IniciarPagoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("iniciar_pago")

    def test_pago_exitoso(self):
        data = {
            "productos": [
                {"nombre": "Producto 1", "precio": "1000"},
                {"nombre": "Producto 2", "precio": "2000.50"}
            ]
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("url_webpay", response.json())

    def test_pago_sin_productos(self):
        data = {"productos": []}
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_pago_precio_invalido(self):
        data = {"productos": [{"nombre": "X", "precio": "no-numero"}]}
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_metodo_get_no_permitido(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertIn("error", response.json())