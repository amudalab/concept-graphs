import web
import json
from doc_ret_edge_enh import rt
        
urls = (
    '/search/(.*)', 'search_handler',
    '/(.*)', 'static_handler'
)
server = web.application(urls, globals())

class search_handler:        
    def GET(self, query):
        return json.dumps(rt(query))
    
class static_handler:
    def GET(self, name):
        raise web.seeother('/static/'+name)

if __name__ == "__main__":
    server.run()