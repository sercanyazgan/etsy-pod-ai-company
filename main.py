import os
import datetime
from crewai import Agent, Task, Crew, Process
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def gorsel_uret(prompt_metni, dosya_adi):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_metni,
            n=1,
            size="1024x1024",
            quality="hd"
        )
        image_url = response.data.url
        return f"![Tasarım]({image_url})\n\n[Görseli Yüksek Kalitede İndirmek İçin Tıklayın]({image_url})"
    except Exception as e:
        return f"Görsel üretilemedi, hata: {str(e)}"

arge_ajani = Agent(
    role='Etsy POD Trend Analisti',
    goal='Etsy verilerine göre en çok satacak ve yüksek canlılıkta DTF baskıya uygun niş konuları bulmak.',
    backstory='Sektörde trendleri önceden tahmin eden e-ticaret uzmanı.',
    verbose=True
)

tasarimci_ajan = Agent(
    role='DTF Baskı Tasarım Uzmanı',
    goal='DTF baskı standartlarına uygun (canlı renkler, temiz kenarlar, kolay dekupe edilebilir arka plan) tişört tasarım görselleri üretmek.',
    backstory='Tekstil baskı teknolojilerine ve yapay zeka görsel üretimine hakim kreatif tasarımcı.',
    verbose=True
)

mockup_ajani = Agent(
    role='Etsy Listeleme ve Mockup Tasarımcısı',
    goal='Üretilen ana tasarımı alıp; Lifestyle model üzerinde, Flatlay tarzında ve detay gösteren yakın çekim satış görselleri (mockup) hazırlamak.',
    backstory='E-ticarette satışı artıran görsel psikolojisini çok iyi bilen fotoğraf ve grafik uzmanı.',
    verbose=True
)

seo_ajani = Agent(
    role='Etsy SEO ve Listeleme Uzmanı',
    goal='Tasarım fikirlerine ve görsellere uygun İngilizce başlık, 13 adet etiket (tags) ve açıklama yazmak.',
    backstory='Etsy algoritmasını çok iyi bilen, ürünleri aramalarda en üst sıraya çıkaran pazarlama uzmanı.',
    verbose=True
)

gorev1 = Task(
    description='Etsy üzerinde DTF baskı ile tişörtlerde harika duracak, renkleri canlı ve bu hafta çok satabilecek 1 adet niş konu belirle.',
    expected_output='Detaylı trend niş konusu raporu.',
    agent=arge_ajani
)

gorev2 = Task(
    description="Belirlenen trend için DALL-E 3 komutu hazırla. Komut kesinlikle şunları içermelidir: 'Vibrant colors, high contrast, clean solid background, sharp edges, suitable for DTF t-shirt printing, isolated design'. Yalnızca İngilizce prompt metnini çıktı olarak ver.",
    expected_output='DALL-E 3 için sadece İngilizce görsel üretim promptu.',
    agent=tasarimci_ajan
)

gorev3 = Task(
    description="Ana tasarıma uygun olarak Etsy'de yüksek satış getirecek 3 farklı mockup promptu hazırla: 1. Lifestyle model wearing the t-shirt close up. 2. Aesthetic flatlay layout of the t-shirt. 3. Macro detailed texture close up. Yalnızca İngilizce prompt metinlerini liste halinde ver.",
    expected_output='3 adet mockup senaryosu içeren İngilizce prompt listesi.',
    agent=mockup_ajani
)

gorev4 = Task(
    description='Ürün için Etsy standartlarında 1 adet İngilizce başlık, 13 adet etiket ve SEO uyumlu ürün açıklaması yaz.',
    expected_output='Başlık, etiketler ve açıklama metni.',
    agent=seo_ajani
)

etsy_sirketi = Crew(
    agents=[arge_ajani, tasarimci_ajan, mockup_ajani, seo_ajani],
    tasks=[gorev1, gorev2, gorev3, gorev4],
    process=Process.sequential
)

if __name__ == "__main__":
    print("🚀 Yeni Nesil Görsel Üretimli Yapay Zeka Şirketi Çalışmaya Başlıyor...")
    sonuc = etsy_sirketi.kickoff()
    
    print("🎨 Görseller Canlı Olarak Üretiliyor...")
    ana_tasarim_linki = gorsel_uret(str(sonuc), "ana_tasarim.png")
    
    rapor_metni = f"""# 📈 ETSY GÜNLÜK ÜRETİM VE MAĞAZA RAPORU

## 🎯 1. AR-GE & SEO SONUÇLARI
{sonuc}

## 👕 2. ÜRETİLEN ANA TASARIM (DTF BASKIYA UYGUN)
{ana_tasarim_linki}
"""
    
    # Tarih bazlı dinamik dosya adı oluşturma
    bugun = datetime.datetime.now().strftime("%d_%m_%Y")
    dosya_adi = f"rapor_{bugun}.md"
    
    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write(rapor_metni)
        
    print(f"✅ İşlem Tamamlandı! Rapor '{dosya_adi}' dosyasına kaydedildi.")
