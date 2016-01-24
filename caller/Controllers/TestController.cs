using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNet.Mvc;

namespace caller.Controllers
{
    [Route("api/[controller]")]
    public class TestController : Controller
    {   
        [HttpGet]
        public async Task<string> Test()
        {
            return await TwilioManager.MakeCall("4013162916", "Hello this is a test of the emergency broadcast system.");
        }
    }
}
