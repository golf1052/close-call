using System;
using System.Text;

namespace caller
{
    public class NumberBundle
    {
        public string Number { get; private set; }
        public string PostId { get; private set; }
        public string Message { get; private set; }
        public string Sequence { get; private set; }
        public string Cons { get; private set; }
        
        public NumberBundle(string number, string message, string postId, string cons)
        {
            Number = number;
            PostId = postId;
            Message = message;
            Random random = new Random();
            StringBuilder sequence = new StringBuilder();
            for (int i = 0; i < 6; i++)
            {
                sequence.Append(random.Next(0, 10));
            }
            Sequence = sequence.ToString();
            Cons = cons;
        }
        
        public string BreakUpSequence()
        {
            StringBuilder builder = new StringBuilder();
            foreach (var c in Sequence)
            {
                builder.Append(c + " ");
            }
            return builder.ToString();
        }
        
        public string FormatNumber()
        {
            return Number.Substring(2);
        }
    }
}