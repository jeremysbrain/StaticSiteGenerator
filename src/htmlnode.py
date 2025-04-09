#from enum import Enum
#class HTMLType(Enum):


class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        html = ""
        for k in self.props:
            html += f" {k}={self.props[k]}"
        return html
    
    def __repr__(self):
        return f"TAG: {self.tag}\nVALUE: {self.value}\nCHILDREN: {self.children}\nPROPS: {self.props}\n\nPROPS_TO_HTML: {self.props_to_html()}"