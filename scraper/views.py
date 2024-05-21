import os
import logging
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer 
from rest_framework.response import Response  
from .scripts.secFilling.sec_filling_full_code import fetch_sec_fillings
from django.views.decorators.csrf import csrf_exempt
from .scripts.secFilling.sec_filling_full_code import fetch_sec_fillings, find_primary_docs

logger = logging.getLogger(__name__)

@api_view(['GET'])
def earning_page(request):
  try:
    if request.method == 'GET': 
      return render(request,'scraped_page.html')
  except Exception as e:
    logger.error("An error occurred in earning_page: %s", str(e))
    return HttpResponse("An error occurred")

@csrf_exempt
@api_view(['GET', 'POST'])
def secFillings_report(request):
  try:
    loadhtmlform = """
    <html>
      <body>
        <form method='POST'>
          <input type='text' name='ticker' placeholder='Enter Ticker Symbol'>
          <select name='report_type'>
            <option value='10-K'>10-K</option>
            <option value='10-Q'>10-Q</option>
            <option value='8-K'>8-K</option>
            <option value='DEF 14A'>DEF 14A</option>
            <option value='SD'>SD</option>
            <option value='SC 13G'>SC 13G</option>
            <!-- Add more options as needed -->
          </select>
          <input type='submit' value='Submit'>
        </form>
      </body>
    </html>
    """
    if request.method == 'POST':
      ticker = request.POST.get('ticker')
      report_type = request.POST.get('report_type')
      try:
        report_path = fetch_sec_fillings(ticker, report_type)
      except Exception as e:
        logger.error("An error occurred in fetch_sec_fillings: %s", str(e))
        return HttpResponse("An error occurred in fetch_sec_fillings")

      try:
        primary_docs = find_primary_docs(report_path)
      except Exception as e:
        logger.error("An error occurred in find_primary_docs: %s", str(e))
        return HttpResponse("An error occurred in find_primary_docs")

      if primary_docs:
        # Assuming primary_docs is a list of dictionaries
        html_content = ""
        for doc in primary_docs:
          doc_path = doc['path']
          if os.path.isfile(doc_path):
            with open(doc_path, 'r') as file:
              html_content += file.read()
        return HttpResponse(html_content)

      if report_path and os.path.isfile(report_path):
        return FileResponse(open(report_path, 'rb'))
      else:
        return HttpResponse("No report found")

    return HttpResponse(loadhtmlform)
  except Exception as e:
    logger.error("An error occurred in secFillings_report: %s", str(e))
    return HttpResponse("An error occurred")