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
}