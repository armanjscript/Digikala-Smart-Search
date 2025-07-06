import streamlit as st
from langchain_ollama import OllamaLLM
from langgraph.graph import Graph, END
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from typing import Dict, TypedDict
import time
import random


# Set up Streamlit UI with RTL and Persian font
st.set_page_config(layout="wide", page_title="جستجوگر هوشمند دیجی‌کالا")

# Custom CSS for RTL and Persian font with proper class targeting
st.markdown("""
<style>
    @font-face {
        font-family: 'BYekan';
        src: url('https://cdn.rawgit.com/rastikerdar/vazir-font/v26.0.2/dist/Vazir.ttf') format('truetype');
    }
    * {
        font-family: 'BYekan', Arial, sans-serif !important;
        direction: rtl !important;
        text-align: right;
    }
    div.stTextInput > div > div > input {
        text-align: right;
        font-size: 16px;
    }
    div.stButton > button {
        width: 100%;
        background-color: #c94604;
        color: #fae77d;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background-color: #e64a19;
        color: white;
        transform: translateY(-2px);
    }
    div.stAlert {
        border-right: 5px solid #4CAF50;
        border-radius: 8px;
    }
    .title-text {
        color: #2b5876;
        text-align: center;
        margin-bottom: 30px;
        font-size: 28px;
        font-weight: bold;
    }
    .result-box {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        background-color: #f9f9f9;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .info-item {
        margin-bottom: 12px;
        font-size: 16px;
    }
    .info-label {
        font-weight: bold;
        color: #2b5876;
    }
    .status-success {
        color: #4CAF50;
        font-weight: bold;
    }
    .status-error {
        color: #f44336;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title with better styling
st.markdown('<h1 class="title-text">🔍 جستجوگر هوشمند دیجی‌کالا</h1>', unsafe_allow_html=True)

# User input with better layout and proper class targeting
col1, col2 = st.columns([4, 1])
with col1:
    user_query = st.text_input("", placeholder="...نام محصول مورد نظر خود را وارد کنید", key="search_input")
with col2:
    search_button = st.button("شروع جستجو", key="search_button")

# Initialize Ollama LLM with Persian language emphasis
llm = OllamaLLM(model="qwen2.5:latest", num_gpu=1)

# Define the agent state
class AgentState(TypedDict):
    user_query: str
    category: str
    search_query: str
    driver: webdriver.Chrome
    status: str

def get_category_and_query(state: AgentState) -> Dict:
    user_query = state.get("user_query", "")
    prompt = f"""
    شما یک دستیار هوشمند فارسی برای سایت دیجی‌کالا هستید. با دقت سوال کاربر را تحلیل کنید و دقیقاً مناسب‌ترین دسته‌بندی را از لیست زیر انتخاب نمایید. همچنین یک عبارت جستجوی دقیق و بهینه به فارسی پیشنهاد دهید.

    دستورالعمل‌های مهم:
    1. برای محصولات دیجیتال دقیق‌ترین دسته را انتخاب کنید (مثلاً برای گوشی موبایل از "موبایل" نه "کالای دیجیتال")
    2. برای لوازم خانگی برقی از "لوازم خانگی برقی" و برای غیربرقی از "خانه و آشپزخانه" استفاده کنید
    3. برای محصولات مراقبت شخصی از "آرایشی بهداشتی" استفاده کنید
    4. برای محصولات کودک از "اسباب بازی، کودک و نوزاد" استفاده کنید
    5. برای مواد غذایی از "سوپر مارکت آنلاین" استفاده کنید
    
    لیست دقیق دسته‌بندی‌ها:
    موبایل (برای گوشی‌های همراه)
    لپ تاپ (برای لپ‌تاپ‌ها و کامپیوترهای همراه)
    کالای دیجیتال (برای لوازم جانبی دیجیتال)
    خانه و آشپزخانه (برای ظروف و لوازم غیربرقی)
    لوازم خانگی برقی (برای یخچال، ماشین لباسشویی، گاز رومیزی، فر، هود و...)
    آرایشی بهداشتی (برای محصولات زیبایی و سلامت)
    خودرو و موتورسیکلت (برای قطعات و لوازم خودرو)
    ابزار آلات و تجهیزات (کلاه ایمنی، کفش ایمنی، پیچ و مهره، انبردست، چکش، مته، فرز، قیچی باغبانی، کیف کمک اولیه، دستکش صنعتی، شیردوش، رگلاتور، کنتاکتور، لولا، شیرآلات، شلنگ، دوش، مغزی و ...)
    مد و پوشاک (برای لباس و کفش)
    طلا و نقره (برای زیورآلات)
    تجهیزات پزشکی و سلامت (برای دستگاه‌های پزشکی یا طبی مثل قوزبند، مچ بند، آرنج بند، مکمل ها، پودر پروتئین، پودر کراتین، قرص، شربت، دستکش لاتکس، کلاه جراحی، سوند، کاندوم، گاز استریل، پیزو، لمینت، مسواک، دارو، وسایل دندانپزشکی، روپوش پزشکی، پد زیر انداز بهداشتی یکبار مصرف، باند زیر گچ، اسپری ضد باکتری و ...)
    کتاب، لوازم تحریر و هنر (برای محصولات فرهنگی)
    ورزش و سفر (برای وسایل ورزشی و مسافرتی)
    کارت هدیه و گیفت کارت (برای کارت‌های هدیه)
    سوپر مارکت آنلاین (برای مواد غذایی)
    اسباب بازی، کودک و نوزاد (برای محصولات کودک)
    محصولات بومی و محلی (برای محصولات محلی)
    کالای کارکرده (برای محصولات دست دوم)
    
    سوال کاربر: {user_query}
    
    پاسخ را دقیقاً به این فرمت بدهید:
    دسته‌بندی: [نام دقیق دسته‌بندی از لیست بالا]
    عبارت جستجو: [عبارت فارسی مناسب برای جستجو]
    """
    
    response = llm.invoke(prompt)
    
    # Parse the response
    category = ""
    search_query = ""
    
    lines = response.split('\n')
    for line in lines:
        if line.startswith("دسته‌بندی:"):
            category = line.split("دسته‌بندی:")[1].strip()
        elif line.startswith("عبارت جستجو:"):
            search_query = line.split("عبارت جستجو:")[1].strip()
    
    # Validate category is from our list
    valid_categories = [
        "موبایل", "لپ تاپ", "کالای دیجیتال", "خانه و آشپزخانه",
        "لوازم خانگی برقی", "آرایشی بهداشتی", "خودرو و موتورسیکلت",
        "ابزار آلات و تجهیزات", "مد و پوشاک", "طلا و نقره",
        "تجهیزات پزشکی و سلامت", "کتاب، لوازم تحریر و هنر",
        "ورزش و سفر", "کارت هدیه و گیفت کارت", "سوپر مارکت آنلاین",
        "اسباب بازی، کودک و نوزاد", "محصولات بومی و محلی", "کالای کارکرده"
    ]
    
    if category not in valid_categories:
        category = "کالای دیجیتال"  # Default fallback
    
    return {
        **state,
        "category": category,
        "search_query": search_query if search_query else user_query,
        "status": "دسته‌بندی و عبارت جستجو تعیین شد"
    }

def init_driver(state: AgentState) -> Dict:
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_experimental_option("detach", True)
    
    try:
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.digikala.com")
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'header'))
        )
        
        return {
            **state,
            "driver": driver,
            "status": "مرورگر آماده شد"
        }
    except Exception as e:
        st.error(f"خطا در راه‌اندازی مرورگر: {str(e)}")
        return {
            **state,
            "driver": None,
            "status": f"خطا در راه‌اندازی مرورگر: {str(e)}"
        }

def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.5)

def human_type(element, text):
    for character in text:
        element.send_keys(character)
        time.sleep(random.uniform(0.05, 0.2))

def navigate_to_category(state: AgentState) -> Dict:
    driver = state.get("driver")
    category = state.get("category", "")
    
    if not driver:
        return {**state, "status": "خطا در اتصال به مرورگر"}
    
    if not category:
        return {**state, "status": "هیچ دسته‌بندی مشخص نشده"}
    
    try:
        menu_span = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-cro-id="header-main-menu"]'))
        )
        
        ActionChains(driver).move_to_element(menu_span).perform()
        time.sleep(1)
        
        menu_container = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.w-full.h-full.flex'))
        )
        
        category_links = []
        attempts = 0
        while attempts < 3 and not category_links:
            category_links = menu_container.find_elements(By.CSS_SELECTOR, 'a[data-cro-id="header-main-menu-categories"]')
            attempts += 1
            time.sleep(1)
        
        if not category_links:
            return {**state, "status": "هیچ دسته‌بندی در منو یافت نشد"}
        
        for link in category_links:
            try:
                ActionChains(driver).move_to_element(link).perform()
                time.sleep(0.2)
                
                p_tag = link.find_element(By.CSS_SELECTOR, 'p.text-body2-strong.text-primary-700')
                if p_tag.text.strip() == category:
                    scroll_to_element(driver, link)
                    link.click()
                    time.sleep(3)
                    return {**state, "status": f"به دسته‌بندی {category} منتقل شد"}
            except Exception:
                continue
        
        return {**state, "status": f"دسته‌بندی {category} در منو یافت نشد"}
        
    except Exception as e:
        return {**state, "status": f"خطا در یافتن دسته‌بندی: {str(e)}"}

def perform_search(state: AgentState) -> Dict:
    driver = state.get("driver")
    search_query = state.get("search_query", "")
    
    if not driver:
        return {**state, "status": "خطا در اتصال به مرورگر"}
    
    if not search_query:
        return {**state, "status": "عبارت جستجو مشخص نشده"}
    
    try:
        search_input = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.NAME, "search-input"))
        )
        
        search_input.clear()
        human_type(search_input, search_query)
        search_input.send_keys(Keys.RETURN)
        time.sleep(3)
        
        return {**state, "status": f"جستجو برای '{search_query}' انجام شد"}
        
    except Exception as e:
        return {**state, "status": f"خطا در جستجو: {str(e)}"}

def display_results(state: AgentState) -> Dict:
    status = state.get("status", "پروسه کامل شد")
    category = state.get("category", "")
    search_query = state.get("search_query", "")
    user_query = state.get("user_query", "")
    
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #2b5876; text-align: center;">نتایج جستجو</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="info-item"><span class="info-label">سوال شما:</span> {user_query}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-item"><span class="info-label">دسته‌بندی انتخاب شده:</span> {category}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="info-item"><span class="info-label">عبارت جستجو:</span> {search_query}</div>', unsafe_allow_html=True)
        status_class = "status-success" if "انجام شد" in status or "منتقل شد" in status else "status-error"
        st.markdown(f'<div class="info-item"><span class="info-label">وضعیت:</span> <span class="{status_class}">{status}</span></div>', unsafe_allow_html=True)
    
    driver = state.get("driver")
    if driver:
        st.markdown(f'<div class="info-item"><span class="info-label">صفحه فعلی:</span> <a href="{driver.current_url}" target="_blank">{driver.current_url}</a></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {**state, "status": "نتایج نمایش داده شد"}

# Build the workflow
workflow = Graph()

# Add nodes
workflow.add_node("initialize", init_driver)
workflow.add_node("get_category", get_category_and_query)
workflow.add_node("navigate_category", navigate_to_category)
workflow.add_node("perform_search", perform_search)
workflow.add_node("display", display_results)

# Define conditional edges
def should_perform_search(state: AgentState) -> str:
    return "display" if "به دسته‌بندی" in state.get("status", "") else "perform_search"

# Define edges
workflow.add_edge("initialize", "get_category")
workflow.add_edge("get_category", "navigate_category")
workflow.add_conditional_edges(
    "navigate_category",
    should_perform_search,
    {
        "perform_search": "perform_search",
        "display": "display"
    }
)
workflow.add_edge("perform_search", "display")
workflow.add_edge("display", END)

# Set entry point
workflow.set_entry_point("initialize")

# Compile the graph
app = workflow.compile()

# Run the agent
if search_button:
    if user_query:
        initial_state = {
            "user_query": user_query,
            "category": "",
            "search_query": "",
            "driver": None,
            "status": "شروع فرآیند"
        }
        
        with st.spinner('در حال پردازش درخواست شما... لطفاً صبر کنید'):
            results = app.invoke(initial_state)
        
        st.success("✅ جستجو با موفقیت انجام شد! نتایج در بالا نمایش داده شده‌اند.")
    else:
        st.warning("لطفاً ابتدا محصول مورد نظر خود را وارد کنید")