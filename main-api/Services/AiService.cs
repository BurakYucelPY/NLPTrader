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

            if (cevap.IsSuccessStatusCode)
            {
                return await cevap.Content.ReadAsStringAsync();
            }
            else
            {
                return "{ \"hata\": \"Python servisine ulaşılamadı.\" }";
            }
        }
        catch (Exception ex)
        {
            return $"{{ \"hata\": \"Bağlantı hatası: {ex.Message}\" }}";
        }
    }
    public async Task<string> FiyatGetir(string sembol)
    {
        try
        {
            var cevap = await _httpClient.GetAsync($"fiyat/{sembol}");

            if (cevap.IsSuccessStatusCode)
            {
                return await cevap.Content.ReadAsStringAsync();
            }
            else
            {
                return "{ \"hata\": \"Fiyat verisi alınamadı.\" }";
            }
        }
        catch (Exception ex)
        {
            return $"{{ \"hata\": \"Bağlantı hatası: {ex.Message}\" }}";
        }
    }
}