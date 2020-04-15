class Document:
    """The class is used to store useful information for a document. 
    You can also write the document to a string for debugging."""
    def __init__(self, url):
        """Constructs a document with a String url."""
        self.url = url
        self.title = None
        self.headers = None
        self.body_hits = None # term -> [list of positions]
        self.body_length = 0
        self.pagerank = 0
        self.anchors = None # term -> anchor_count
        self.debugStr = ""
        
    def __iter__(self):
        for u in self.url:
            yield u
            
    def __str__(self):  
        result = [];
        NEW_LINE = "\n"
#         result.append("url: "+ self.url + NEW_LINE);
        if (self.title is not None): result.append("title: " + self.title + NEW_LINE);
        if (self.headers is not None): result.append("headers: " + str(self.headers) + NEW_LINE);
        if (self.body_hits is not None): result.append("body_hits: " + str(self.body_hits) + NEW_LINE);
        if (self.body_length != 0): result.append("body_length: " + str(self.body_length) + NEW_LINE);
        if (self.pagerank != 0): result.append("pagerank: " + str(self.pagerank) + NEW_LINE);
        if (self.anchors is not None): result.append("anchors: " + str(self.anchors) + NEW_LINE);
        return " ".join(result)

    __repr__ = __str__    
