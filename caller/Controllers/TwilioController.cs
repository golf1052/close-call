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
        public ContentResult GenerateTwiml()
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
                    XElement gather = new XElement("Gather");
                    gather.SetAttributeValue("action", "http://e1e5bf2b.ngrok.io/api/Voice/Input");
                    gather.SetAttributeValue("timeout", "10");
                    gather.SetAttributeValue("numDigits", "6");
                    gather.Add(GetSay("Please enter the following digits within 10 seconds." + bundle.BreakUpSequence()));
                    twimlPair.Item2.Add(gather);
                    twimlPair.Item2.Add(GetSay(bundle.Message));
                    return Content(twimlPair.Item1.ToString(), "application/xml");
                }
            }
            // if we can't find the number then reject the call
            twimlPair.Item2.Add(new XElement("Reject"));
            return Content(twimlPair.Item1.ToString(), "application/xml");
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
        [Route("Voice/Input")]
        public ContentResult ProcessGather()
        {
            var twimlPair = GetStandardTwiml();
            if (Request.Form.ContainsKey("To") && Request.Form.ContainsKey("Digits"))
            {
                string number = Request.Form["To"];
                string digits = Request.Form["Digits"];
                NumberBundle bundle = TwilioManager.GetMessage(number);
                if (bundle != null)
                {
                    if (bundle.Sequence == digits)
                    {
                        
                        twimlPair.Item2.Add(new XElement("Reject"));
                        return Content(twimlPair.Item1.ToString(), "application/xml");
                    }
                }
            }
            return Content(twimlPair.Item1.ToString(), "application/xml");
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
        
        private XElement GetSay(string message)
        {
            XElement element = new XElement("Say", message);
            element.SetAttributeValue("voice", "alice");
            element.SetAttributeValue("language", "en-US");
            return element;
        }
    }
}
