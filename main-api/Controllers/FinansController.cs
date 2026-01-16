using Microsoft.AspNetCore.Mvc;
using main_api.Services;

namespace main_api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class FinansController : ControllerBase
{
    private readonly AiService _aiService;

    public FinansController(AiService aiService)
    {
        _aiService = aiService;
    }

    [HttpGet("{sembol}")]
    public async Task<IActionResult> FiyatGetir(string sembol)
    {
        var sonuc = await _aiService.FiyatGetir(sembol);
        return Ok(sonuc);
    }
}