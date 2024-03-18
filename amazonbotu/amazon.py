import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode

# Telegram botunuzun token'ını buraya ekleyin
TOKEN = "6884841990:AAFc2gOv785d6_O_SYBqxgpz094xjwI2iHE"
def get_amazon_discounts():
    url = "https://www.amazon.com.tr/s?k=indirim"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    response = requests.get(url, headers=headers)
    discount_products = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("div", class_="s-result-item")

        for product in products:
            title = product.find("h2").text.strip()
            price_element = product.find("span", class_="a-price")

            if price_element:
                price = float(
                    price_element.find("span", class_="a-offscreen").text.replace("₺", "").replace(",", ".").strip())
                regular_price = float(
                    price_element.find("span", class_="a-text-price").find("span", class_="a-offscreen").text.replace(
                        "₺", "").replace(",", ".").strip())

                discount_percentage = ((regular_price - price) / regular_price) * 100

                if discount_percentage > 50:
                    currency = "₺"
                    link = "https://www.amazon.com.tr" + product.find("a", class_="a-link-normal").get("href")

                    discount_products.append((title, price, discount_percentage, link))

    return discount_products


def start(update, context):
    update.message.reply_text("Merhaba! Yüzde 50 üzerindeki indirimleri kontrol ediyorum, biraz bekleyin...")

    discounts = get_amazon_discounts()

    if discounts:
        for product in discounts:
            message = f"Başlık: {product[0]}\nFiyat: {product[1]}₺\nİndirim Yüzdesi: %{product[2]}\nLink: {product[3]}"
            update.message.reply_text(message, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text("Üzgünüm, yüzde 50 üzerinde indirim bulunamadı.")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
