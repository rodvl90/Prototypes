import os
from pprint import pprint

# from dotenv import load_dotenv
from langchain.document_loaders import ConfluenceLoader

CONFLUENCE_API_KEY = "ATATT3xFfGF01jDzMqzJhMT7LehO8lwUegfs7tnFMiTu6j5X9eePUMOf3io7D-BbFStHjbVO68M2rJOLiFUQZ6zBcgYtZbWZDoQ9ixHFlfIwZjVMvUG_Jh1UXCcbSvxjvbMbfbBUFT_o-gDewDB3jxUCXhaI32hOkrXqaAHKw51y6orQDqQdCvQ=54DF9915"
loader = ConfluenceLoader(
    url="https://7heightsstudio.atlassian.net/wiki", username="d.vlad90@gmail.com", api_key=CONFLUENCE_API_KEY
)
documents = loader.load(space_key="CS", limit=50)

pprint(documents)