using System;
using System.Text;

namespace caller
{
    public class NumberBundle
    {
        public string Number { get; private set; }
        public string Message { get; private set; }
        public string Sequence { get; private set; }
        
        public NumberBundle(string number, string message)
        {
            Number = number;
            Message = message;
            Random random = new Random();
            StringBuilder sequence = new StringBuilder();
            for (int i = 0; i < 6; i++)
            {
                sequence.Append(random.Next(0, 10));
            }
            Sequence = sequence.ToString();
        }
    }
}