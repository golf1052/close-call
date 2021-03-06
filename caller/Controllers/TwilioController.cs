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
        [Route("Call")]
        public async Task<bool> Call()
        {
            if (Request.Form.ContainsKey("cons"))
            {
                string cons = Request.Form["cons"];
                if (cons == "facebook")
                {
                    if (Request.Form.ContainsKey("number"))
                    {
                        if (Request.Form.ContainsKey("post_id") &&
                        Request.Form.ContainsKey("post"))
                        {
                            await TwilioManager.MakeCall(Request.Form["number"], Request.Form["post"], Request.Form["post_id"], cons);
                            return true;
                        }
                        else
                        {
                            await TwilioManager.MakeCall(Request.Form["number"], "We will Venmo money to a random person.", null, cons);
                            return true;
                        }
                    }
                }
                else if (cons == "venmo")
                {
                    if (Request.Form.ContainsKey("number"))
                    {
                        await TwilioManager.MakeCall(Request.Form["number"], "We will Venmo money to a random person.", null, cons);
                        return true;
                    }
                }
            }
            return false;
        }
        
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
                    twimlPair.Item2.Add(GetSay("Good morning!"));
                    twimlPair.Item2.Add(new XElement("Pause"));
                    // twimlPair.Item2.Add(GetGather("10", bundle.BreakUpSequence()));
                    string[] split = bundle.Message.Split('|');
                    twimlPair.Item2.Add(GetSay(split[0]));
                    twimlPair.Item2.Add(new XElement("Pause"));
                    if (split.Length > 1)
                    {
                        string join = string.Empty;
                        for (int i = 1; i < split.Length; i++)
                        {
                            join += split[i];
                        }
                        twimlPair.Item2.Add(GetSay(join));
                    }
                    twimlPair.Item2.Add(GetGather("10", bundle.BreakUpSequence()));
                    return Content(twimlPair.Item1.ToString(), "application/xml");
                }
            }
            // if we can't find the number then reject the call
            twimlPair.Item2.Add(new XElement("Reject"));
            return Content(twimlPair.Item1.ToString(), "application/xml");
        }
        
        [HttpPost]
        [Route("Voice/Status")]
        public async Task Status()
        {
            if (Request.Form.ContainsKey("To"))
            {
                string number = Request.Form["To"];
                NumberBundle bundle = TwilioManager.GetMessage(number);
                if (bundle != null)
                {
                    // if (Request.Form["AnsweredBy"] == "human")
                    // {
                    //     string callStatus = Request.Form["CallStatus"];
                    //     if (callStatus == "completed" ||
                    //     callStatus == "in-progress" ||
                    //     callStatus == "failed")
                    //     {
                    //     }
                    // }
                    await Fail(bundle);
                }
            }
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
                        TwilioManager.RemoveNumber(number);
                        twimlPair.Item2.Add(GetSay("That was a close call. You are free."));
                        // twimlPair.Item2.Add(new XElement("Reject"));
                        return Content(twimlPair.Item1.ToString(), "application/xml");
                    }
                }
                string[] split = bundle.Message.Split('|');
                twimlPair.Item2.Add(GetSay(split[0]));
                twimlPair.Item2.Add(new XElement("Pause"));
                if (split.Length > 1)
                {
                    string join = string.Empty;
                    for (int i = 1; i < split.Length; i++)
                    {
                        join += split[i];
                    }
                    twimlPair.Item2.Add(GetSay(join));
                }
                twimlPair.Item2.Add(GetGather("5", bundle.BreakUpSequence()));
                return Content(twimlPair.Item1.ToString(), "application/xml");
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

        private XElement GetGather(string timeout, string sequence)
        {
            XElement element = new XElement("Gather", GetSay("Please enter the following digits within 10 seconds. " + sequence));
            element.SetAttributeValue("action", TwilioManager.ngrokUrl + "/api/Twilio/Voice/Input");
            element.SetAttributeValue("timeout", timeout);
            element.SetAttributeValue("numDigits", "6");
            return element;
        }
        
        private async Task Fail(NumberBundle bundle)
        {
            if (bundle.Cons == "facebook")
            {
                await Failures.Facebook(bundle.FormatNumber(), bundle.PostId);
            }
            else if (bundle.Cons == "venmo")
            {
                await Failures.Venmo(bundle.FormatNumber());
            }
        }
    }
}
