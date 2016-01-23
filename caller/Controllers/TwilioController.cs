using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNet.Mvc;
using System.Xml.Linq;
using Newtonsoft.Json.Linq;
using System.Diagnostics;

namespace caller.Controllers
{
    [Route("api/[controller]")]
    public class TwilioController : Controller
    {
        [HttpPost]
        [Route("Generate")]
        public string GenerateTwiml()
        {
            var twimlPair = GetStandardTwiml();
            if (Request.Form.ContainsKey("To"))
            {
                string number = Request.Form["To"];
                Debug.WriteLine(number);
                NumberBundle bundle = TwilioManager.GetMessage(number);
                Debug.WriteLine(bundle);
                if (bundle != null)
                {
                    XElement say = new XElement("Say");
                    say.SetAttributeValue("voice", "alice");
                    say.SetAttributeValue("language", "en-US");
                    say.SetValue(bundle.Message);
                    twimlPair.Item2.Add(say);
                    return twimlPair.Item1.ToString();
                }
            }
            // if we can't find the number then reject the call
            twimlPair.Item2.Add(new XElement("Reject"));
            return twimlPair.Item1.ToString();
        }
        
        [HttpPost]
        [Route("Voice/Incoming")]
        public string HandleIncomingCalls()
        {
            var twimlPair = GetStandardTwiml();
            if (Request.Form.ContainsKey("To"))
            {
                string number = Request.Form["To"];
                NumberBundle bundle = TwilioManager.GetMessage(number);
                if (bundle != null)
                {
                }
            }
            // if we can't find the number then reject the call
            twimlPair.Item2.Add(new XElement("Reject"));
            return twimlPair.Item1.ToString();
        }
        
        [HttpPost]
        [Route("SMS/Incoming")]
        public string HandleIncomingSMS()
        {
            return null;
        }
        
        private Tuple<XDocument, XElement> GetStandardTwiml()
        {
            XDocument twiml = new XDocument();
            twiml.Declaration = new XDeclaration("1.0", "utf-8", "");
            XElement response = new XElement("Response");
            twiml.Add(response);
            return new Tuple<XDocument, XElement>(twiml, response);
        }
    }
}
