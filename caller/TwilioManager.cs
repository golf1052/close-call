using System;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json.Linq;
using System.Net.Http.Headers;
using System.Net.Http;

namespace caller
{
    public static class TwilioManager
    {
        public static string ngrokUrl = "http://accd3f59.ngrok.io";
        static string baseUrl = "https://{0}:{1}@api.twilio.com/2010-04-01";
        static string twilioSid = "";
        static string twilioAuth = "";
        static string twilioNumber = "";
        
        private static Dictionary<string, NumberBundle> messages;
        
        static TwilioManager()
        {
            using (StreamReader reader = new StreamReader(File.OpenRead("credentials.json")))
            {
                JObject credentials = JObject.Parse(reader.ReadToEnd());
                twilioSid = (string)credentials["twilio_sid"];
                twilioAuth = (string)credentials["twilio_auth_token"];
                twilioNumber = (string)credentials["twilio_number"];
            }
            messages = new Dictionary<string, NumberBundle>();
        }
        
        public static async Task<string> MakeCall(string number, string message, string postId, string cons)
        {
            number = "+1" + number;
            string url = string.Format(baseUrl, twilioSid, twilioAuth) + string.Format("/Accounts/{0}/Calls.json", twilioSid);
            HttpClient client = new HttpClient();
            List<KeyValuePair<string, string>> values = new List<KeyValuePair<string, string>>();
            values.Add(new KeyValuePair<string, string>("From", twilioNumber));
            values.Add(new KeyValuePair<string, string>("To", number));
            values.Add(new KeyValuePair<string, string>("Url", ngrokUrl + "/api/twilio/generate"));
            values.Add(new KeyValuePair<string, string>("StatusCallback", ngrokUrl + "/api/Twilio/Voice/Status"));
            values.Add(new KeyValuePair<string, string>("StatusCallbackEvent", "completed"));
            values.Add(new KeyValuePair<string, string>("IfMachine", "Hangup"));
            if (messages.ContainsKey(number))
            {
                messages.Remove(number);
            }
            messages.Add(number, new NumberBundle(number, message, postId, cons));
            HttpResponseMessage response = await client.PostAsync(url, new FormUrlEncodedContent(values));
            return await response.Content.ReadAsStringAsync();
        }
        
        public static NumberBundle GetMessage(string number)
        {
            if (messages.ContainsKey(number))
            {
                return messages[number];
            }
            else
            {
                return null;
            }
        }
        
        public static void RemoveNumber(string number)
        {
            if (messages.ContainsKey(number))
            {
                messages.Remove(number);
            }
        }
    }
}