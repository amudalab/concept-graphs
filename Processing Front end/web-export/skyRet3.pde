color bg;
int i=0,j=0;
int w,h;
int A[];
int n=3,avg=0;
int screen;
void setup()
{  page1();
}
void page1()
{  size(displayWidth,displayHeight);
   w=width/4;h=height/2; 
   background(0,255,153);
   screen=0;
   noStroke();
   rect(w,h-h/4,2*w,h/8,4);
}
void page2()
{ size(displayWidth,displayHeight); 
  w=width/2;h=height/2; 
  background(100,10,120);
  //noStroke();
  //fill(255,255,50);
  //ellipseMode(CENTER);
  //ellipse(w,h,w,w);
  /*A=new int[n];
  A[0]=5;
  A[1]=3;
  A[2]=4;
  for(int i=0;i<n;i++)
  {  avg+=A[i];
  }*/
  //avg=avg/n;
  //print(avg);
  stroke(100,100,23);
  polygonset(w,h,w/8,6);
  polygonset(w+3*w/8,h,w/8,6);
  polygonset(w-3*w/8,h,w/8,6);
}
void draw()
{             
  
}
void mousePressed()
{ if(sq(mouseX-w)+sq(mouseY-h)<=sq(w))
  { print("VARUN");  
    //ellipse( w,h,(A[i]/avg)*w,(A[i]/avg)*w);
    i++;
  }
 // print("IN",mouseX,"#",mouseY," ");
}
void polygonset(float x,float y,float r,int np)
{  float attract=r+r*cos(60);
   float rt3=sqrt(3)*r;
   float rx=r+r/2;
   polygon(x,y,r,np);
   polygon(x,y-rt3,r,np);
   polygon(x+rx,y-rt3/2,r,np);
   polygon(x+rx,y+rt3/2,r,np);
   polygon(x,y+rt3,r,np);
   polygon(x-rx,y+rt3/2,r,np);
   polygon(x-rx,y-rt3/2,r,np);
}
void polygon(float x, float y, float radius, int npoints) 
{
  float angle = TWO_PI / npoints;
  beginShape();
  for (float a = 0; a < TWO_PI; a += angle) {
    float sx = x + cos(a) * radius;
    float sy = y + sin(a) * radius;
    vertex(sx, sy);
  }
  endShape(CLOSE);
}


