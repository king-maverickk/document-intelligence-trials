# import libraries
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest


endpoint = os.getenv("AZURE_ENDPOINT")
key = os.getenv("AZURE_KEY")

def analyze_layout():
    # document
    formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-layout.pdf"

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout", AnalyzeDocumentRequest(url_source=formUrl
    ))

    # ^^ "prebuilt-layout" == https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/layout?view=doc-intel-4.0.0&tabs=sdks%2Csample-code
    # other prebuilt models. This is great so far.

    result: AnalyzeResult = poller.result()

    if result.styles and any([style.is_handwritten for style in result.styles]):
        print("Document contains handwritten content")
    else:
        print("Document does not contain handwritten content")

    if result.tables:
            for table_idx, table in enumerate(result.tables):
                print(
                    f"Table # {table_idx} has {table.row_count} rows and "
                    f"{table.column_count} columns"
                )
                if table.bounding_regions:
                    for region in table.bounding_regions:
                        print(
                            f"Table # {table_idx} location on page: {region.page_number} is {region.polygon}"
                        )
                for cell in table.cells:
                    print(
                        f"...Cell[{cell.row_index}][{cell.column_index}] has text '{cell.content}'"
                    )
                    if cell.bounding_regions:
                        for region in cell.bounding_regions:
                            print(
                                f"...content on page {region.page_number} is within bounding polygon '{region.polygon}'"
                            )

    print("----------------------------------------")
    
    for page in result.pages:
        print(
            f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}"
        )

if __name__ == "__main__":
    analyze_layout()