import json
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from common.models import Career


class DialogFlowWebhookView(APIView):
    def post(self, request):
        req = request.data

        response_text = ""
        intent = req["queryResult"]["intent"]["displayName"]

        if intent == "Idemo":
            response_text = "Tôi tên là Bùi Khánh Huy"
        else:
            response_text = f"There are no fulfillment responses defined for Intent {intent}"

        results = []
        for i in range(0, 5):
            results.append(
                {
                    "payload": {
                        "richContent": [
                            [
                                {
                                    "type": "info",
                                    "title": "Công Ty Cổ Phần Ẩm Thực Mặt Trời Vàng",
                                    "subtitle": "💸18tr - 20tr | 📌TP.HCM | ⌛18/12/2024",
                                    "image": {
                                        "src": {
                                            "rawUrl": "https://cdn1.vieclam24h.vn/tvn/images/old_employer_avatar/images/c8a43407d9219a5ff09f205d07d23d08_5cd0f536e479a_1557198134.png"
                                        }
                                    },
                                    "actionLink": "http://localhost:3000/viec-lam/quan-binh-thanh-giam-sat-mua-hang"
                                }
                            ]
                        ]
                    }
                }
            )

        res = {
            "fulfillmentMessages": results
        }

        return Response(status=status.HTTP_200_OK, data=res)
