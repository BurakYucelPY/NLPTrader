using System.Text;
using System.Text.Json;
using main_api.Models;

namespace main_api.Services;

public class AiService
{
    private readonly HttpClient _httpClient;

    public AiService(HttpClient httpClient)
    {
        _httpClient = httpClient;
        // Python servisinin adresi
        _httpClient.BaseAddress = new Uri("http://127.0.0.1:8000/");
    }

    // 1. Analiz Fonksiyonu
    public async Task<string> AnalizEt(string metin)
    {
        var gidecekVeri = new { metin = metin };
        var jsonPaket = new StringContent(
            JsonSerializer.Serialize(gidecekVeri), 
            Encoding.UTF8, 
            "application/json"
        );

        try
        {
            var cevap = await _httpClient.PostAsync("analiz", jsonPaket);
            if (cevap.IsSuccessStatusCode) return await cevap.Content.ReadAsStringAsync();
            else return "{ \"hata\": \"Python servisine ulaşılamadı.\" }";
        }
        catch (Exception ex) { return $"{{ \"hata\": \"Bağlantı hatası: {ex.Message}\" }}"; }
    }

    // 2. Fiyat Getirme Fonksiyonu
    public async Task<string> FiyatGetir(string sembol)
    {
        try
        {
            var cevap = await _httpClient.GetAsync($"fiyat/{sembol}");
            if (cevap.IsSuccessStatusCode) return await cevap.Content.ReadAsStringAsync();
            else return "{ \"hata\": \"Fiyat verisi alınamadı.\" }";
        }
        catch (Exception ex) { return $"{{ \"hata\": \"Bağlantı hatası: {ex.Message}\" }}"; }
    }

    // 3. Haber/Piyasa Analizi Getirme Fonksiyonu
    public async Task<string> PiyasaDurumuGetir()
    {
        try
        {
            var cevap = await _httpClient.GetAsync("piyasa-durumu");
            if (cevap.IsSuccessStatusCode) return await cevap.Content.ReadAsStringAsync();
            else return "{ \"hata\": \"Haber verisi alınamadı.\" }";
        }
        catch (Exception ex) { return $"{{ \"hata\": \"Bağlantı hatası: {ex.Message}\" }}"; }
    }

    // 4. SSE Stream Proxy - Haberleri Python'dan stream olarak al
    public async Task<HttpResponseMessage> PiyasaDurumuStreamGetir()
    {
        var request = new HttpRequestMessage(HttpMethod.Get, "piyasa-durumu-stream");
        return await _httpClient.SendAsync(request, HttpCompletionOption.ResponseHeadersRead);
    }
    // 5. Grafik Verisi Getirme Fonksiyonu
    public async Task<string> GrafikGetir(string sembol, string periyot)
    {
        try
        {
            var cevap = await _httpClient.GetAsync($"grafik/{sembol}?periyot={periyot}");
            if (cevap.IsSuccessStatusCode) return await cevap.Content.ReadAsStringAsync();
            else return "{ \"hata\": \"Grafik verisi alınamadı.\" }";
        }
        catch (Exception ex) { return $"{{ \"hata\": \"Bağlantı hatası: {ex.Message}\" }}"; }
    }
}