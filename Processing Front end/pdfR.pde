import processing.pdf.*;
import java.awt.Desktop;
import java.io.File;
import java.io.IOException;

class pdfR
{  public void display(String path)
   { if(Desktop.isDesktopSupported())
     { try
       { File myFile = new File(path);
         Desktop.getDesktop().open(myFile);
       }
       catch(IOException ex) 
       {
        // no application registered for PDFs
       }
     } 
   }
}
