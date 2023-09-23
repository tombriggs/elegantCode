#include <iostream>
using namespace std;

   int main()
   {
   	int i,j,sum=0;
   	for (i=0;i<1000;i++)
   	{
   	
   		 if (i%5==0||i%3==0)
   		 sum+=i;
	   }
	   cout<<"\n";
	   cout<<"\n sum  : ";
	   cout<<sum;
	   cin.get();
   }
