from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def copy_web_content(url, filename):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize WebDriver with Service
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        page_source = driver.page_source
        # Save it as an HTML file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(page_source)
    finally:
        driver.quit()

# Directory to save HTML files
output_dir = "scraped_html"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# List of URLs
urls = [
    "https://aws.amazon.com/agreement/",
    "https://aws.amazon.com/service-terms/",
    "https://aws.amazon.com/legal/",
    "https://agreementservice.svs.nike.com/us/en_us/rest/agreement?agreementType=termsOfUse&uxId=com.nike.commerce.nikedotcom.web&country=US&language=en&requestType=redirect",
    "https://www.adidas.com/us/help/us-company-information/what-are-the-terms-and-conditions",
    "https://www.davidson.edu/offices-and-services/technology-innovation/it-guidelines-policies/davidson-college-technology-terms-service",
    "https://www.creditkarma.com/about/terms202011",
    "https://www.capitalone.com/digital/corporate-terms/",
    "https://www.discover.com/discover-terms-of-use/",
    "https://customersupport.spirit.com/en-US/category/article/KA-01195",
    "https://www.bcbs.com/terms-conditions",
    "https://www.selenium.dev/documentation/about/copyright/",
    "https://www.bankofamerica.com/online-banking/service-agreement.go",
    "https://stripe.com/legal/ssa",
    "https://stripe.com/legal/consumer",
    "https://stripe.com/legal/connect-account",
    "https://www.linkedin.com/legal/user-agreement",
    "https://www.linkedin.com/legal/l/service-terms",
    "https://www.grammarly.com/terms",
    "https://www.grammarly.com/terms-2022",
    "https://www.grammarly.com/terms/customer-business-agreement",
    "https://www.amazon.com/gp/help/customer/display.html?nodeId=202140280"
]


# Iterate over each URL and save its content
for url in urls:
    filename = os.path.join(output_dir, url.split('//')[1].replace('/', '_').replace('?', '_').replace('&', '_') + '.html')
    copy_web_content(url, filename)
