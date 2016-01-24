using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Net.Http;

namespace caller
{
    public static class Failures
    {
        public static async Task Facebook(string number, string postId)
        {
            Dictionary<string, string> values = new Dictionary<string, string>();
            values.Add("number", number);
            values.Add("post_id", postId);
            await Bridge(values, "facebook");
        }
        
        public static async Task Venmo(string number)
        {
            Dictionary<string, string> values = new Dictionary<string, string>();
            values.Add("number", number);
            await Bridge(values, "venmo");
        }
        
        private static async Task Bridge(Dictionary<string, string> values, string bridgeName)
        {
            HttpClient client = new HttpClient();
            await client.PostAsync("http://localhost:5000/bridge/" + bridgeName, new FormUrlEncodedContent(values));
        }
    }
}