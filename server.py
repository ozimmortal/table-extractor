import extractor
from fasthtml.common import *

app,rt= fast_app()
@rt('/')
async def get():
    inpt_group=Group(Input(type='text',name='url'),Button('extract',cls='contrast'))
    return Titled('Welcome!',Card(
        Form(inpt_group,hx_post='/add',target_id='lists',hx_swap='innerHtml',hx_indicator='#spinner')),
        Card(
            Div(Article(id='spinner',aria_busy="true",cls='htmx-indicator'),id='lists')
        )
        )
@rt('/add')
async def ppost(url:str):
    try:
        table = extractor.Extractor(url).extract_table()
        table_path = extractor.Extractor(url).save_to_file()
        head =Thead(Tr(*[Th(i) for i in table[0]]))
        body = Tbody(*[Tr(*[Td(i) for i in row]) for row in table[1:]])
        return Div(A('download table',cls='contrast',href=f'/table/{table_path}'),Table(head,body))
    except Exception as e:
        return 'No table found'

@rt("/table/{fname:path}")
async def get(fname:str): 
    return FileResponse(f'{fname}')
serve()