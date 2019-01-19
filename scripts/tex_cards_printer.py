from tex_printer import *
from skill_matrix import *
from project_printer import *
from employment_printer import *
from cv.time import *
from cv.skill_experience import *
from tex.elements import *
from tex.cv_project import *
from tex.cv_employment import *
from tex.cv_headcolumn import *

PT_IN_MM = 2.83465

# In pt
GRID_V_SPACING = 15
GRID_H_SPACING = 12
PAGE_H_MARGIN = 10*PT_IN_MM



# A4 =  210 mm x  297 mm =  595 pt x  842 pt
class TexCardsPrinter(TexPrinter):
  V_SPACING = 15
  # CARD_WIDTH = (595 - 4 * V_SPACING)/3
  # CARD_HEIGHT = 206
  CARD_WIDTH = (595 - 2 * PAGE_H_MARGIN - 2* GRID_H_SPACING) / 3
  CARDS_IN_ROW = 3
  HEADER_HEIGHT = 24
  HOR_SPACING = 4
  
  def print_scientific_pubs(self, pubs, scopus_count):
    summary_str = '%d total' % len(pubs)
    if scopus_count:
      summary_str += ', incl. %d Scopus' % scopus_count
    self.write([r'\itemhead{\textbf{Scientific Publications}}',
      r'',
      r'\itemsubhead{%s}' % summary_str,
      r''])

    self.writeln(r'\begin{itemize-cv}')
    for pub in pubs:
      if pub['visible']:
        is_scopus = '\scopus' if (('source' in pub) and (pub['source'] == 'Scopus')) else ''
        self.writeln(r'\item \rmfamily %d --- %s // %s %s' % (int(pub['year']), pub['title'], pub['journal'], is_scopus))

    self.writeln(r'\end{itemize-cv}')

  def print_popoular_pubs(self, pubs):    
    years = int(pubs[0]['year']) - int(pubs[-1]['year']) + 1
    summary_str = '%d total, avg. %.1f publicatons / year' % (len(pubs), float(len(pubs))/years)
    # self.write(['\t\\textbf{Recent Popular Publications} (%s):' % summary_str,
    #   '\\begin{itemize-noindent}'
    # ])
    self.write([r'\itemhead{\textbf{Popular Publications}}',
      r'',
      r'\itemsubhead{%s}' % summary_str,
      r''])

    self.writeln(r'\begin{itemize-cv}')
    for pub in pubs:
      if pub['visible']:
        self.writeln(r'\item \rmfamily %d --- %s // %s \href{%s}{[link]}' % (int(pub['year']), pub['title'], pub['source'], pub['url']))
    self.writeln(r'\end{itemize-cv}')
  
  def print_conferences(self, conferences):
    years = int(conferences[0]['year']) - int(conferences[-1]['year']) + 1
    summary_str = '%d total, avg. %.1f presentations / year' % (len(conferences), float(len(conferences))/years)
    conf_strs = []
    

    self.write([r'\itemhead{\textbf{Conference Presentations}}',
      r'',
      r'\itemsubhead{%s}' % summary_str,
      r'',
      r'\begin{itemize-cv}'
    ])

    for conf in conferences:
      self.write([
        r'\item %s (%s, %d)' % (conf['name'], conf['location'], conf['year'])
      ])

    self.write([
      r'\end{itemize-cv}'
    ])

  def print_activities(self, profile):
    if profile.scientificPubs:
      with MinipageElement(self, '{}pt'.format(self.CARD_WIDTH)):
        self.print_scientific_pubs(profile.scientificPubs, profile.scopus_publication_count())
      self.write([
        r'\vspace{%dpt}' % GRID_V_SPACING,
      ])
  
    if profile.popularPubs:
      with MinipageElement(self, '{}pt'.format(self.CARD_WIDTH)):
        self.print_popoular_pubs(profile.popularPubs)
      self.write([
        r'\vspace{%dpt}' % GRID_V_SPACING,
      ])

    if profile.conferences:
      with MinipageElement(self, '{}pt'.format(self.CARD_WIDTH)):
        self.print_conferences(profile.conferences)
      self.write([
        r'\vspace{%dpt}' % GRID_V_SPACING,
      ])
  
    if profile.traits:
      with MinipageElement(self, '{}pt'.format(self.CARD_WIDTH)):
        self.write([r'\itemhead{\textbf{Personal}}',
          r'',
          r'\begin{itemize-cv}'])

        for trait in profile.traits:
          self.write([r'\item \textbf{%s:} %s' % (trait['name'], trait['details'])])

        self.write([r'\end{itemize-cv}'])


  def print_data(self, profile, file):
    EMPLOYMENT_CARD_HEIGHT = 100
   
    out_dir = self.rootDir
    self.write([
      r'\documentclass[10pt]{ucv-cards}',
      r'\usepackage[a4paper, top=10mm, bottom=20mm, left=%dpt, right=%dpt]{geometry}' % (PAGE_H_MARGIN, PAGE_H_MARGIN)
    ])

    # self.image_path('img/correct.svg')

    self.write([
      r'\begin{document}',
    #   r'\setlength\parindent{0pt}'
      ])


    self.write([
      r'\setlength{\parindent}{0pt}',
      r'\setlength{\columnsep}{%dpt}' % GRID_H_SPACING,
      # r'\setlength{\intextsep}{0pt}',
      # r'\columnratio{0.33}',
      # r'\begin{paracol}{2}'
      # r'\begin{wrapfigure}{l}{180pt}',
      # r'\begin{minipage}[t][0.98\textheight]{180pt}'
    ])
    
    self.write([
      r'\begin{textblock}{%d}[0, 0](%f,%f)' % (self.CARD_WIDTH, PAGE_H_MARGIN, PT_IN_MM*10),
      r'\begin{minipage}{%dpt}' % (self.CARD_WIDTH-2),
      
    ])
    
    HeadColumn(self, profile)
    # self.print_head_column(profile)

    self.write([
      r'\rule{%dpt}{2pt}' % self.CARD_WIDTH,
      r'\end{minipage}\hspace{1pt}\vrule width 2pt',
      r'',
      r'\end{textblock}'
    ])

    
    header_hoffset = self.CARD_WIDTH + GRID_H_SPACING - 6
    SectionHeading(self, 'Relevant Projects', 'In order of relevance', header_hoffset)
    
    with SectionElement(self):
      self.write([
        r'\phantom{x}',
        r'',
        r'\columnbreak'
      ])
      for project in profile.projects:
        with MinipageElement(self, '{}pt'.format(self.CARD_WIDTH)):
          ProjectElement(self, project)
        VSpacingElement(self, GRID_V_SPACING)
    
    ## DEBUG
    self.write([
      r'\clearpage'
    ])
    

    SectionHeading(self, 'Employment History', 'Total %.1f years in industrial development' % profile.total_employment_time().years())

    with SectionElement(self):
      for employment in profile.employments:
        with MinipageElement(self, '{}pt'.format(self.CARD_WIDTH)):
          EmploymentBlock(self, employment)
        VSpacingElement(self, GRID_V_SPACING)

    
    SectionHeading(self, 'Activities and Personal', 'Only recent is presented')
    with SectionElement(self):
      self.print_activities(profile)

    self.write([
      r'\end{document}'
    ])
