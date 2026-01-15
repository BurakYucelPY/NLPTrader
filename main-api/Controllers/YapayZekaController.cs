using Microsoft.AspNetCore.Mvc;
using main_api.Models;

namespace main_api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class YapayZekaController : ControllerBase
{
    [HttpPost("analiz-et")]
    public IActionResult AnalizEt([FromBody] AnalizIstegi istek)
    {
        return Ok(new { mesaj = "Mesaj alındı", gelen_veri = istek.Metin });
    }
}