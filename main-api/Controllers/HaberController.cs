using Microsoft.AspNetCore.Mvc;
using main_api.Services;

namespace main_api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class HaberController : ControllerBase
{
    private readonly AiService _aiService;

    public HaberController(AiService aiService)
    {
        _aiService = aiService;
    }

    [HttpGet("analiz")]
    public async Task<IActionResult> Getir()
    {
        var sonuc = await _aiService.PiyasaDurumuGetir();
        return Ok(sonuc);
    }

    [HttpGet("stream")]
    public async Task StreamGetir()
    {
        Response.ContentType = "text/event-stream";
        Response.Headers["Cache-Control"] = "no-cache";
        Response.Headers["Connection"] = "keep-alive";

        try
        {
            var pythonCevap = await _aiService.PiyasaDurumuStreamGetir();
            using var stream = await pythonCevap.Content.ReadAsStreamAsync();
            await stream.CopyToAsync(Response.Body);
        }
        catch (Exception ex)
        {
            await Response.WriteAsync($"data: {{\"hata\": \"{ex.Message}\"}}\n\n");
        }
    }
}