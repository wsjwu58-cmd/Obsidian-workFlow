# 取余

```
#include<stdio.h>
int main()
{
	char code[] = {'\x1f', '\x12', '\x1d', '(', '0', '4', '\x01', '\x06', '\x14', '4', ',',
		'\x1b', 'U', '?', 'o', '6', '*', ':', '\x01', 'D', ';', '%', '\x13' };
	int i,len;
	len = sizeof(code);
	for (i = len - 2; i >= 0; i--)
		code[i] = code[i] ^ code[i + 1];
	for (i = 0; i < len; i++)
	{
		code[i] -= i;
		while (code[i] < 33)
		{
			code[i] += 128;
		}
	}
	printf("%s", code);
}
```

```
#include<stdio.h>
#include<string.h>
int main (){
  char strCode[] = "~4G~M:=WV7iX,zlViGmu4?hJ0H-Q*";

for(int i = 28; i >= 0; i --)
{
  char tmp = strCode[i] - 32 - strCode[(i * i + 123) % 21];
  while (tmp < 32) tmp += 96;
  strCode[i] = tmp;
}
printf("%s",strCode);





 return 0;
}
```

```
c = [
    144,
    163,
    158,
    177,
    121,
    39,
    58,
    58,
    91,
    111,
    25,
    158,
    72,
    53,
    152,
    78,
    171,
    12,
    53,
    105,
    45,
    12,
    12,
    53,
    12,
    171,
    111,
    91,
    53,
    152,
    105,
    45,
    152,
    144,
    39,
    171,
    45,
    91,
    78,
    45,
    158,
    8]
flag=""
b=179
for i in range(42):
    for j in range(32,128):
        if j*33 % b == c[i]:
            print(chr(j))
```

