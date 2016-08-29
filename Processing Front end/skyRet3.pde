
// GLOBAL DECLARATIONS ----------------------->>>>>>>>>>>>> 
color bg;
int i=0,j=0;
float tx,ty,tw,w8;
int w,h;
int n=3,avg=0;
int screen;
String query="";
class points
{  public float x,y;
  public points(float a,float b)
  { x=a;y=b;}
};
ArrayList<points> hex=new ArrayList<points>();

class data
{  public int id;
   public String masp;
   public ArrayList<String> sasp;
   public ArrayList<ArrayList<String>> docname;
};
data asp[];int sizeofdata;

// ON START APPLICATION ----------------------->>>>>>>>>>>>> 
void setup()
{  page1();
}


// SCREEN HANDLERS ----------------------->>>>>>>>>>>>> 
void page1()
{  size(displayWidth,displayHeight);
   w=width/4;h=height/2; 
   //background(0,255,153);
   PImage img;
   tint(255,128);
   img=loadImage("paper.jpg");
   //img=loadImage("p2.jpg");
   //img=loadImage("p5.jpg");
   image(img,0,0);
   screen=1;
   rect(w,h-h/4,2*w,h/8,4);
   textSize(30);
   textAlign(BOTTOM);
   tx=w+2;ty=h-h/6;
   tw/=2;
}
void page2(String query)
{ size(displayWidth,displayHeight); 
  screen=2;
  w=width/2;h=height/2;w8=width/16;
  background(100,10,120);
  noStroke();
  fill(255,255,50);
  stroke(100,100,23);
  polygonset(w/2,h,w/8,6);
  fill(0,0,0);
  textSize(10);
  loadcontent(query);
  drawpoly(w/8,6);
  readcontent();
  //openpdf("C:\\Users\\Varun Shankar S\\Desktop\\Gsearch\\speech recognition\\hbka.pdf");
}


// LOOPER ----------------------->>>>>>>>>>>>> 
void draw()
{              
}


// EVENT HANDLERS ----------------------->>>>>>>>>>>>> 
void keyPressed()
{ if(screen==1)
  { 
    if((key>='A'&&key<='Z')||(key>='a'&&key<='z'))
    { if(query.length()<=15)
      { fill(255,255,255);
        rect(w,h-h/4,2*w,h/8,4);
        fill(232,50,83);
        query=query+key;
        text(query,tx,ty);
      }
    }
    else if(key==8)
    {
    }
    else if(key=='\n')
    { int found=checkfile(query);
      if(found==1)
        page2(query);
      else
      { query="";
        fill(255,255,255);
        rect(w,h-h/4,2*w,h/8,4);
      }
    }
  }  
}
points prev,cur;boolean hflag=false,mflag=true,f2flag=false;int map=0,clk=0;
void mouseMoved()
{ mflag=true;map=0;
  for(int i=0;i<sizeofdata;i++)
  { points p=hex.get(i);
    if(sq(mouseX-p.x)+sq(mouseY-p.y)<=sq(w8))
     { if(hflag)
       { fill(255,255,50);
         polygon(prev.x,prev.y,w/8,6); 
         int ind=checkindex(prev);
         displaycontent(ind,3);
       }
       fill(220,20,60);
       polygon(p.x,p.y,w8,6);
       displaycontent(map,3);
       prev=new points(p.x,p.y);
       hflag=true;
       mflag=false;
     }
     if(mflag!=false)
     {   map++;
     }
  }
}
void mouseClicked()
{  
  print("MM:",map);
  if(screen==2)
   { if(mouseButton==LEFT)
      { if(map<sizeofdata)
        { clk=map;
          f2flag=true;
          float xx=hex.get(clk).x,yy=hex.get(clk).y;
          fill(255,255,0);
          polygon(w,h/2,w/4,6);
          displaycontent(clk,100);
        } 
        
      }
     else if(mouseButton==RIGHT)
     { print("VARUN");
     }
   }
}


// HELPER FUNCTIONS ----------------------->>>>>>>>>>>>>
int checkfile(String str)
{  JSONArray values;
   values = loadJSONArray("index.json");
   JSONObject files = values.getJSONObject(0);
   JSONArray keys= files.getJSONArray("query");
   int found=0;
   for(int i=0;i<keys.size();i++)
   {   String f=keys.getString(i);
      if(str.equals(f)==true)
      { found=1;
        break;
      }
   }
   return found;
}
int checkindex(points p)
{  int in=-1;
   for(int i=0;i<sizeofdata;i++)
   {  if(hex.get(i).x==p.x&&hex.get(i).y==p.y)
      { in=i;
        break;
      }
   }
   return in;
}
void displaycontent(int map,int n)
{  if(map>=0 && map<sizeofdata)
   { int s=1,k=20;
     if(n>3)
        k=40;
     fill(0,0,0);
     textSize(18);
     print("",map);
     if(n>3)
       text(asp[map].masp,13*w/15,h/2);
     else
       text(asp[map].masp,13*hex.get(map).x/15,hex.get(map).y);
     textSize(11);
     for(int j=0;j<asp[map].sasp.size() && j<=n;j++)
     { if(n>3)
         text(asp[map].sasp.get(j),13*w/15,h/2-k*s);
       else
         text(asp[map].sasp.get(j),13*hex.get(map).x/15,hex.get(map).y-k*s);
       s=s*-1;
       if(s==1)
         k+=10;
       if(n>3)
         k+=10;
     }
   }
}
void loadcontent(String file)
{ JSONArray values;
  file=file+".json";
  values = loadJSONArray(file);
  sizeofdata=values.size();
  asp=new data[values.size()];
  for (int i = 0; i < values.size(); i++)
  { JSONObject aspect = values.getJSONObject(i);
    asp[i]=new data();
    asp[i].id = aspect.getInt("id");
    asp[i].masp = aspect.getString("aspect");
    JSONArray subkey= aspect.getJSONArray("subkeys");
    JSONArray docn = aspect.getJSONArray("doc");
    asp[i].sasp=new ArrayList<String>();
    asp[i].docname=new ArrayList<ArrayList<String>>();
    for(int j=0;j<subkey.size();j++)
    { asp[i].sasp.add(subkey.getString(j));
    }
    for(int j=0;j<docn.size();j++)
    { ArrayList<String> temp=new ArrayList<String>();
      JSONArray docnm=docn.getJSONArray(j);
      for(int k=0;k<docnm.size();k++)
      { temp.add(docnm.getString(k));
      }
      asp[i].docname.add(temp);
      print("\nDOC:",docnm);
    }
    print("SSS:",docn);
    print("\n");
  }   
  tempread();
}

void readcontent()
{  fill(0,0,0);
   for(int i=0;i<sizeofdata;i++)
   { //print(asp[i].id+" "+asp[i].masp+" "+asp[i].sasp);
     int s=1,k=20;
     textSize(18);
     text(asp[i].masp,13*hex.get(i).x/15,hex.get(i).y);
     textSize(11);
     for(int j=0;j<asp[i].sasp.size() && j<=3;j++)
     { text(asp[i].sasp.get(j),13*hex.get(i).x/15,hex.get(i).y-k*s);
       s=s*-1;
       if(s==1)
         k+=10;
     }
   }
}
void polygonset(float x,float y,float r,int np)
{  float rt3=sqrt(3)*r;
   float rx=r+r/2;
   hex.add(new points(x,y));
   hex.add(new points(x,y-rt3));
   hex.add(new points(x+rx,y-rt3/2));
   hex.add(new points(x+rx,y+rt3/2));
   hex.add(new points(x,y+rt3));
   hex.add(new points(x-rx,y+rt3/2));
   hex.add(new points(x-rx,y-rt3/2));
 
   x=w-3*w/6;y=h;
   hex.add(new points(x,y));
   hex.add(new points(x,y-rt3));
   hex.add(new points(x,y+rt3));
   
   x=w+3*w/6;y=h;
   hex.add(new points(x,y));
   hex.add(new points(x,y-rt3));
   hex.add(new points(x,y+rt3));
}
void openpdf(String path)
{  pdfR p=new pdfR();
   p.display(path);
}
void tempread()
{  for(int i=0;i<sizeofdata;i++)
   { for(int j=0;j<asp[i].docname.size();j++)
     { ArrayList<String> temp=asp[i].docname.get(j);
       for(int k=0;k<temp.size();k++)
       { print(temp.get(k));print("AAAA");
       }
       print("\n");
     } 
     print("\n");
   }
   print("S",sizeofdata);
}
/*void displaydoctitle(int map)
{   if(map>0 && map<sizeofdata)
    {  asp[map].docname
    }
}*/
void drawpoly(float r,int np)
{  fill(255,0,0);  
   for(int i=0;i<sizeofdata;i++)
   { polygon(hex.get(i).x,hex.get(i).y,r,np);
     fill(255,255,50);
   }
   polygon(w,h/2,w/4,6);
   noStroke();
   rectMode(CORNERS);
   fill(220,100);
   rect(1.3*w,20,2*w-w/25,2*h-h/6);
}
void polygon(float x, float y, float radius, int npoints) 
{ float angle = TWO_PI / npoints;
  beginShape();
  for (float a = 0; a < TWO_PI; a += angle)
  { float sx = x + cos(a) * radius;
    float sy = y + sin(a) * radius;
    vertex(sx, sy);
  }
  endShape(CLOSE);
}
