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
        datos = json.loads(request.body)  # Convierte el JSON del body en diccionario Python
        productos = datos.get("productos", [])  # Extrae los productos seleccionados

        if not productos:
            return JsonResponse({"error": "No se seleccionaron productos."}, status=400)

        # Calcula el total sumando los precios de los productos
        try:
            total = sum(round(float(p["precio"])) for p in productos)
        except (ValueError, KeyError, TypeError) as e:
            return JsonResponse({"error": f"Precio inválido: {str(e)}"}, status=400)

        # Define datos requeridos por Transbank para iniciar la transacción
        buy_order = f"orden{request.META['REMOTE_ADDR'].replace('.', '')}"  # Crea orden basada en IP
        session_id = "session123"  # Valor fijo, pero se puede personalizar
        return_url = "http://127.0.0.1:8000/pago_exitoso/"  # URL a la que redirige Transbank tras pagar

        # Configura opciones del entorno de integración de Transbank
        options = WebpayOptions(
            commerce_code="597055555532",  # Código de comercio de prueba
            api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",  # API Key de prueba
            integration_type=IntegrationType.TEST  # Ambiente de prueba
        )

        transaction = Transaction(options)  # Crea instancia para transacción

        try:
            # Llama al SDK de Transbank para crear la transacción
            response = transaction.create(buy_order, session_id, total, return_url)
            return JsonResponse({
                "url_webpay": response['url'] + "?token_ws=" + response['token'],
                "token": response['token']
            })
        except TransbankError as e:
            print("❌ Error en la creación del pago:", e.message)
            return JsonResponse({"error": e.message}, status=500)

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
                {"nombre": "Taladro Inalámbrico", "precio": "12000"},
                {"nombre": "Destornillador Eléctrico", "precio": "5000"}
            ]
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("url_webpay", body)
        self.assertTrue(
            body["url_webpay"].startswith("https://"),
            msg="La URL de Webpay debe empezar con https://"
        )

    def test_pago_sin_productos(self):
        response = self.client.post(
            self.url,
            data=json.dumps({"productos": []}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_pago_precio_invalido(self):
        response = self.client.post(
            self.url,
            data=json.dumps({"productos": [{"nombre": "X", "precio": "abc"}]}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_metodo_get_no_permitido(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertIn("error", response.json())
