using Microsoft.AspNetCore.Mvc;
using main_api.Models;
using main_api.Services;

namespace main_api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class YapayZekaController : ControllerBase
{
    private readonly AiService _aiService;
    public YapayZekaController(AiService aiService)
    {
        _aiService = aiService;
    }

    [HttpPost("analiz-et")]
    public async Task<IActionResult> AnalizEt([FromBody] AnalizIstegi istek)
    {
        // Gelen veriyi servise gönder
        var sonuc = await _aiService.AnalizEt(istek.Metin);
        return Ok(sonuc);
    }
}