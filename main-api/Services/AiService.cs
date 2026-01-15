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
                // Python'dan gelen cevabı oku ve geri döndür
                return await cevap.Content.ReadAsStringAsync();
            }
            else
            {
                return "{ \"hata\": \"Python servisine ulaşılamadı veya hata döndü.\" }";
            }
        }
        catch (Exception ex)
        {
            return $"{{ \"hata\": \"Bağlantı hatası: {ex.Message}\" }}";
        }
    }
}