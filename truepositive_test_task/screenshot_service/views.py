from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from truepositive_test_task.utils.screenshots import screenshot_maker


class ScreenshotAPIView(APIView):
    def post(self, request):
        url = request.data.get('url')
        if not url:
            return Response({'error': 'URL not provided'}, status=status.HTTP_400_BAD_REQUEST)
        screenshot = screenshot_maker.create_screenshot(url)
        return Response({'screenshot': screenshot}, status=status.HTTP_201_CREATED)

    def get(self, request):
        return Response(data=..., status=status.HTTP_200_OK)


