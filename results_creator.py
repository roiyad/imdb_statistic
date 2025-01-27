from pptx import Presentation
class ResultCreator():

    def __init__(self):
        self.pres = Presentation()

    def add_slide(self, slide_data: dict, slide_type: int):
        slide = self.pres.slide_layouts[slide_type]
        page = self.pres.slides.add_slide(slide)
        for key, text in slide_data.items():
            if key == 'title':
                page.shapes.title.text = text
            elif key == 'content':
                page.placeholders[1].text = text


        self.pres.save('check_file.pptx')
