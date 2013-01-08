import unittest
from srcgen.hypertext import html, head, title, link, body, h1, p, COMMENT, TEXT, ATTR, UNESCAPED, Unescaped


class TestPython(unittest.TestCase):
    def test_basic(self):
        with html as doc:
            with head:
                title("das title")
                link(rel = "foobar", type="text/css")
            
            with body:
                with h1.title(z=7, x=5, y=6):
                    TEXT("hello", "world")
                with p:
                    TEXT("i am a para&graph\nwith newl<i>nes")
                    UNESCAPED("&nbsp;")
                    ATTR(data_role = "description")
        
        self.assertEqual(str(doc), """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>das title</title>
    <link rel="foobar" type="text/css"/>
  </head>
  <body>
    <h1 class="title" x="5" y="6" z="7">hello world</h1>
    <p data-role="description">
i am a para&amp;graph
with newl&lt;i&gt;nes
&nbsp;
    </p>
  </body>
</html>""")
    
    def test_escaping(self):
        with p as doc:
            cp = Unescaped("&copy;")
            nbsp = Unescaped("&nbsp;")
    
            TEXT(cp + " 2013 tomer")
            TEXT(Unescaped("&copy; %s and %s") % ("2013 < tomer", nbsp))
            TEXT("&copy; %s and %s" % ("2013 < tomer", nbsp))
            TEXT(Unescaped("<") * 4)
        
        self.assertEqual(str(doc), """<p>
&copy; 2013 tomer
&copy; 2013 &lt; tomer and &nbsp;
&amp;copy; 2013 &lt; tomer and &amp;nbsp;
<<<<
</p>""")

    def test_comments(self):
        with body as doc:
            COMMENT("generated by john")
            with h1:
                TEXT("heading")
            with p:
                TEXT("paragraph")
            with COMMENT:
                with p:
                    TEXT("all of this is commented out")
                TEXT("and this too")
                COMMENT("even i'm commented!")
        
        self.assertEqual(str(doc), """<body>
  <!-- generated by john -->
  <h1>heading</h1>
  <p>paragraph</p>
  <!--
    <p>all of this is commented out</p>
and this too
    <!-- even i&apos;m commented! -- >
  -->
</body>""")


if __name__ == "__main__":
    unittest.main()

