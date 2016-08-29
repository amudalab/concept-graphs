#include<iostream>
#include<fstream>
#include<string>
using namespace std;
class data
{ public:
	string str;
}w[300],k[300],words[300];
int main()
{	fstream f,g,a;
	int temp,keyl=0,wordl=0;
	string s;
	int i=0,j;
	f.open("newtestpaper.txt",ios::in);
	g.open("keywordZ.txt",ios::in);
	a.open("keyfinal.txt",ios::out);
	while(!f.eof())
	{ getline(f,s);
	  w[i++].str=s;wordl++;
	  //cout<<w[i-1].str<<endl;
	}
	f.close();
	i=0;
	while(!g.eof())
	{ getline(g,s);
	  if(s!="")
	  {k[i++].str=s;keyl++;
	   //cout<<k[i-1].str<<endl;
	  }
	}
	g.close();
	for(i=0;i<300;i++)
		words[i].str="";
	//cout<<wordl<<" "<<keyl<<endl;
	//cin>>temp;
	int inw=0,ink=0,inl=0,fl=0,fg=1,found=0,n,m;
	for(i=0;i<wordl;)
	{ j=0;fl=0;fg=1;found=0;
	  cout<<"1Iter: "<<i<<endl;
	  while(fg!=0)
	  { fl=0;
	    //cout<<"1j:"<<j<<" i:"<<i<<" word:"<<k[j].str<<" inw:"<<w[inw].str<<" inl:"<<inl<<" fl:"<<fl<<" fg:"<<fg<<endl;
	    if(w[i].str==k[j].str)
	  	{ ink=j;
	  	  //cout<<"2ink:"<<ink<<" i:"<<i<<" word:"<<k[ink].str<<" inw:"<<w[inw].str<<" inl:"<<inl<<" fl:"<<fl<<" fg:"<<fg<<endl;
		  for(inw=i;k[ink].str!="0";inw++)
	  	  { //cout<<"3ink:"<<ink<<" i:"<<i<<" word:"<<k[ink].str<<" inw:"<<w[inw].str<<" inl:"<<inl<<" fl:"<<fl<<" fg:"<<fg<<endl;
			if(w[inw].str==k[ink].str)
	  	    { ink++;
	  	      words[inl].str=words[inl].str+w[inw].str+" ";
	  	      //cout<<"1word: "<<words[inl].str<<endl;
	  	      //cin>>temp;
	  	    }
	  	  	else
	  		{ fl=1;words[inl].str="";break;
	  		}
	  	  }
	  	  if(fl==0)
	  	  { inl++;fg=0;//cout<<"HIT"<<fg<<" "<<fl<<" "<<inl;
			i=inw;found=1;}
	  	  else
	  	  j++;
		  //inw=i;//i=inw;}
		}
		else
		{ for(m=j;k[m].str!="0"&&m<keyl;m++)
			{  //cout<<"2m:"<<m<<"ink:"<<ink<<" j:"<<j;
		  //cout<<k[m].str<<" ";
		  //cout<<endl;
		  //cin>>temp;
		  }
		  j=m+1;
		  //ink=j;
		 /* if(m==139)
		  { cout<<"old i:"<<i;i=inw;cout<<" i:"<<i;break;}*/
		  //cout<<"2j:"<<j<<endl;
		  if(!(m<keyl))
		  	break;
		  
		}
	  }
	  if(found==0)
	  	i++;
	}
	for(i=0;i<inl;i++)
	{	cout<<words[i].str<<endl;
		a<<words[i].str<<"\n";
	}
		
	return 0;
}
