class GeminiPredictor:
    def __init__(self, model_name):
        self.model_name = model_name
        self.api_key = "AIzaSyB4ptLib_l0yrs3LsylaXcROe_kGRcA8V0"
        self.model = self.initialize_model()

    def initialize_model(self):
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        return genai.GenerativeModel(model_name=self.model_name)

    def predict_match(self, match_data):
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 200,
            "response_mime_type": "text/plain",
        }

        combined_input = (
            "Sen bir iddaa ve futbol bahis uzmanısın. Analizlerinde istatistiksel verileri, takım form durumunu, sakat ve cezalı oyuncuları, son maç performanslarını ve karşılıklı maç geçmişini dikkate alarak tahmin yap.\n"
            "Cevaplarını aşağıdaki formatta, detaylı ve güvenilir şekilde ver:\n"
            "Maç Verisi: {match_data}\n"
            "Maç Sonucu (Detaylı analizle, örn: Ev sahibi kazanır, beraberlik, deplasman kazanır ve skor tahmini):\n"
            "Kupon Önerisi (En güvenilir bahis seçeneği ve kısa açıklaması):\n"
            "Oran Tahmini (Yüksek olasılıkla gerçekleşecek tahmin için yaklaşık oran):\n"
            "Tahmin Güven Skoru (1-10 arası, ne kadar emin olduğun):\n"
            "Kısa Analiz (Tahmininin nedenlerini 2-3 cümleyle açıkla):\n"
            "Örnek:\n"
            "Maç Sonucu: 2-1 Ev sahibi kazanır\n"
            "Kupon Önerisi: 2,5 üst (Her iki takım da hücumda formda)\n"
            "Oran Tahmini: 1.85\n"
            "Tahmin Güven Skoru: 8\n"
            "Kısa Analiz: Ev sahibi son 5 maçta yenilmedi ve hücumda etkili. Konuk ekip savunmada zayıf.\n"
            f"Şimdi bu maç için detaylı tahmin yap:\nMaç Verisi: {match_data}"
        )
        response = self.model.generate_content(combined_input, generation_config=generation_config)
        return response.text.strip()


predictor = GeminiPredictor(model_name="gemini-1.0-pro")