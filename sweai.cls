%% sweai.cls — Custom document class for "Software Engineering in the Age of AI"
%% Based on memoir class with XeLaTeX font support
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{sweai}[2025/01/01 Software Engineering in the Age of AI]

%% ---------- Base class ----------
\LoadClass[11pt,openright,twoside,letterpaper]{memoir}

%% ---------- Essential packages ----------
\RequirePackage{fontspec}
\RequirePackage{xcolor}
\RequirePackage{graphicx}
\RequirePackage{grffile}
\RequirePackage{hyperref}
\RequirePackage{url}
\RequirePackage{tcolorbox}
\tcbuselibrary{skins,breakable,listings}
\RequirePackage{enumitem}
\RequirePackage{booktabs}
\RequirePackage{tabularx}
\RequirePackage{longtable}
\RequirePackage{multirow}
\RequirePackage{listings}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{microtype}
\RequirePackage{tikz}
\RequirePackage{caption}
\RequirePackage{subcaption}
\RequirePackage{float}
\RequirePackage{fancyvrb}
\RequirePackage{etoolbox}
\RequirePackage[backend=biber,style=numeric,sorting=none]{biblatex}

%% ---------- Color palette (O'Reilly-inspired) ----------
\definecolor{oreillyred}{HTML}{C4362A}
\definecolor{oreillyteal}{HTML}{00758F}
\definecolor{oreillydark}{HTML}{1A1A2E}
\definecolor{oreillyblue}{HTML}{2D6A8F}
\definecolor{oreillygray}{HTML}{4A4A4A}
\definecolor{oreillylightgray}{HTML}{F5F5F5}
\definecolor{oreillymedgray}{HTML}{E0E0E0}
\definecolor{oreillywarm}{HTML}{F9F6F0}
\definecolor{oreillygreen}{HTML}{2E7D32}
\definecolor{oreillyyellow}{HTML}{F9A825}
\definecolor{oreillyorange}{HTML}{E65100}
\definecolor{codebg}{HTML}{F8F8F2}
\definecolor{codeframe}{HTML}{DDDDDD}

%% ---------- Fonts ----------
%% Use Source family — unique, professional, highly readable
\setmainfont{Source Serif 4}[
  Path = fonts/source-serif/,
  Extension = .otf,
  UprightFont = *-Regular,
  BoldFont = *-Bold,
  ItalicFont = *-It,
  BoldItalicFont = *-BoldIt,
  Numbers = OldStyle,
]

\setsansfont{Source Sans 3}[
  Path = fonts/source-sans/,
  Extension = .otf,
  UprightFont = *-Regular,
  BoldFont = *-Bold,
  ItalicFont = *-It,
  BoldItalicFont = *-BoldIt,
]

\setmonofont{Source Code Pro}[
  Path = fonts/source-code-pro/,
  Extension = .otf,
  UprightFont = *-Regular,
  BoldFont = *-Bold,
  ItalicFont = *-It,
  BoldItalicFont = *-BoldIt,
  Scale = 0.88,
]

%% ---------- Page layout ----------
\settrimmedsize{11in}{8.5in}{*}
\setlrmarginsandblock{1.2in}{0.9in}{*}
\setulmarginsandblock{1.0in}{1.2in}{*}
\setheadfoot{\baselineskip}{2\baselineskip}
\setheaderspaces{*}{1.5\baselineskip}{*}
\checkandfixthelayout

%% ---------- Chapter style ----------
\makechapterstyle{sweai}{%
  \chapterstyle{default}
  \renewcommand*{\chapnumfont}{\sffamily\bfseries\fontsize{60}{72}\selectfont\color{oreillyteal}}
  \renewcommand*{\chaptitlefont}{\sffamily\bfseries\HUGE\color{oreillydark}}
  \renewcommand*{\printchaptername}{}
  \renewcommand*{\chapternamenum}{}
  \renewcommand*{\printchapternum}{%
    \begin{tikzpicture}[remember picture, overlay]
      \fill[oreillyteal!8] (current page.north west) rectangle ([yshift=-3.5cm]current page.north east);
      \node[anchor=north east, inner sep=0pt] at ([xshift=-1cm,yshift=-0.3cm]current page.north east) {%
        \chapnumfont\thechapter
      };
    \end{tikzpicture}
    \vspace{1cm}
  }
  \renewcommand*{\afterchapternum}{\par\vskip 0.5\baselineskip}
  \renewcommand*{\printchaptertitle}[1]{%
    \chaptitlefont ##1
    \par\vskip 0.3\baselineskip
    {\color{oreillyteal}\rule{\textwidth}{2pt}}
  }
}
\chapterstyle{sweai}

%% ---------- Part style ----------
\renewcommand{\partnamefont}{\sffamily\bfseries\Huge\color{oreillyteal}}
\renewcommand{\partnumfont}{\sffamily\bfseries\fontsize{72}{86}\selectfont\color{oreillyteal!30}}
\renewcommand{\parttitlefont}{\sffamily\bfseries\fontsize{30}{36}\selectfont\color{oreillydark}}
\renewcommand{\beforepartskip}{\vspace*{3cm}}
\renewcommand{\midpartskip}{\par\vskip 1cm{\color{oreillyteal}\rule{0.5\textwidth}{2pt}}\par\vskip 1cm}

%% ---------- Section styles ----------
\setsecheadstyle{\sffamily\bfseries\Large\color{oreillydark}}
\setsubsecheadstyle{\sffamily\bfseries\large\color{oreillyblue}}
\setsubsubsecheadstyle{\sffamily\bfseries\normalsize\color{oreillygray}}

%% ---------- Headers and footers ----------
\makepagestyle{sweaipage}
\makeevenhead{sweaipage}{\sffamily\small\thepage}{}{\sffamily\small\leftmark}
\makeoddhead{sweaipage}{\sffamily\small\rightmark}{}{\sffamily\small\thepage}
\makeevenfoot{sweaipage}{}{}{}
\makeoddfoot{sweaipage}{}{}{}
\makeheadrule{sweaipage}{\textwidth}{\normalrulethickness}
\pagestyle{sweaipage}

%% ---------- Table of contents styling ----------
\renewcommand{\cftpartfont}{\sffamily\bfseries\large\color{oreillyteal}}
\renewcommand{\cftchapterfont}{\sffamily\bfseries\color{oreillydark}}
\renewcommand{\cftsectionfont}{\sffamily\color{oreillygray}}

%% ---------- Hyperref configuration ----------
\hypersetup{
  colorlinks=true,
  linkcolor=oreillyteal,
  citecolor=oreillyblue,
  urlcolor=oreillyred,
  pdfauthor={},
  pdftitle={Software Engineering in the Age of AI},
  pdfsubject={Software Engineering, LLMs, AI},
  pdfkeywords={software engineering, LLMs, AI, machine learning, agents},
  bookmarksnumbered=true,
  bookmarksopen=true,
}

%% ---------- Code listing style ----------
\lstdefinestyle{sweaicode}{
  backgroundcolor=\color{codebg},
  basicstyle=\ttfamily\small,
  breakatwhitespace=false,
  breaklines=true,
  captionpos=b,
  commentstyle=\color{oreillygreen}\itshape,
  keywordstyle=\color{oreillyteal}\bfseries,
  stringstyle=\color{oreillyred},
  numbers=left,
  numberstyle=\tiny\color{oreillygray},
  numbersep=8pt,
  showspaces=false,
  showstringspaces=false,
  frame=single,
  rulecolor=\color{codeframe},
  xleftmargin=1.5em,
  framexleftmargin=1.5em,
  tabsize=4,
  aboveskip=1em,
  belowskip=1em,
}
\lstset{style=sweaicode}

%% Python language definition for listings
\lstdefinelanguage{Python}{
  keywords={False, None, True, and, as, assert, async, await, break, class, continue, def, del, elif, else, except, finally, for, from, global, if, import, in, is, lambda, nonlocal, not, or, pass, raise, return, try, while, with, yield},
  morekeywords={self, cls, int, float, str, list, dict, tuple, set, bool, bytes, type, object},
  sensitive=true,
  morecomment=[l]{\#},
  morecomment=[s]{"""}{"""},
  morecomment=[s]{'''}{'''},
  morestring=[b]",
  morestring=[b]',
}

%% ---------- Custom environments ----------

%% Key Takeaway box
\newtcolorbox{keytakeaway}[1][Key Takeaway]{%
  enhanced,
  breakable,
  colback=oreillyteal!5,
  colframe=oreillyteal,
  coltitle=white,
  fonttitle=\sffamily\bfseries,
  title={#1},
  arc=2mm,
  boxrule=0.8pt,
  left=8pt,
  right=8pt,
  top=6pt,
  bottom=6pt,
  before skip=1em,
  after skip=1em,
}

%% Warning/Caution box
\newtcolorbox{cautionbox}[1][Caution]{%
  enhanced,
  breakable,
  colback=oreillyred!5,
  colframe=oreillyred,
  coltitle=white,
  fonttitle=\sffamily\bfseries,
  title={$\triangle$ #1},
  arc=2mm,
  boxrule=0.8pt,
  left=8pt,
  right=8pt,
  top=6pt,
  bottom=6pt,
  before skip=1em,
  after skip=1em,
}

%% Tip/Note box
\newtcolorbox{tipbox}[1][Tip]{%
  enhanced,
  breakable,
  colback=oreillygreen!5,
  colframe=oreillygreen!80!black,
  coltitle=white,
  fonttitle=\sffamily\bfseries,
  title={\textbf{$\star$} #1},
  arc=2mm,
  boxrule=0.8pt,
  left=8pt,
  right=8pt,
  top=6pt,
  bottom=6pt,
  before skip=1em,
  after skip=1em,
}

%% Case Study box
\newtcolorbox{casestudy}[1][Case Study]{%
  enhanced,
  breakable,
  colback=oreillywarm,
  colframe=oreillyorange,
  coltitle=white,
  fonttitle=\sffamily\bfseries,
  title={#1},
  arc=2mm,
  boxrule=0.8pt,
  left=8pt,
  right=8pt,
  top=6pt,
  bottom=6pt,
  before skip=1em,
  after skip=1em,
}

%% Interview Question box
\newcounter{interviewq}[chapter]
\renewcommand{\theinterviewq}{\thechapter.\arabic{interviewq}}

\newtcolorbox{interviewquestion}[1][]{%
  enhanced,
  breakable,
  colback=oreillylightgray,
  colframe=oreillyblue,
  coltitle=white,
  fonttitle=\sffamily\bfseries,
  title={Question \refstepcounter{interviewq}\theinterviewq\ifstrempty{#1}{}{ — #1}},
  arc=2mm,
  boxrule=0.8pt,
  left=8pt,
  right=8pt,
  top=6pt,
  bottom=6pt,
  before skip=1em,
  after skip=1em,
}

%% Interview Solution box
\newtcolorbox{interviewsolution}{%
  enhanced,
  breakable,
  colback=white,
  colframe=oreillymedgray,
  fonttitle=\sffamily\bfseries\color{oreillydark},
  title={Solution},
  arc=2mm,
  boxrule=0.5pt,
  left=8pt,
  right=8pt,
  top=6pt,
  bottom=6pt,
  before skip=0.5em,
  after skip=1em,
}

%% Difficulty indicator
\newcommand{\difficulty}[1]{%
  \par\noindent\textbf{\sffamily\color{oreillygray}Difficulty:}
  \ifnum#1=1 {\color{oreillygreen}$\bullet$}{\color{oreillymedgray}$\bullet\bullet\bullet$}\fi
  \ifnum#1=2 {\color{oreillyyellow}$\bullet\bullet$}{\color{oreillymedgray}$\bullet\bullet$}\fi
  \ifnum#1=3 {\color{oreillyorange}$\bullet\bullet\bullet$}{\color{oreillymedgray}$\bullet$}\fi
  \ifnum#1=4 {\color{oreillyred}$\bullet\bullet\bullet\bullet$}\fi
  \par
}

%% Company tag
\newcommand{\companytag}[1]{%
  \tikz[baseline=(tag.base)]{\node[fill=oreillyteal!10, draw=oreillyteal!40, rounded corners=2pt, inner sep=3pt, font=\sffamily\scriptsize\color{oreillyteal}] (tag) {#1};}%
}

%% Interviewer insight box
\newtcolorbox{interviewerinsight}{%
  enhanced,
  breakable,
  colback=oreillyteal!3,
  colframe=oreillyteal!40,
  fonttitle=\sffamily\bfseries\small\color{oreillyteal},
  title={What the Interviewer Is Really Looking For},
  arc=2mm,
  boxrule=0.5pt,
  left=8pt,
  right=8pt,
  top=4pt,
  bottom=4pt,
  before skip=0.5em,
  after skip=1em,
}

%% ---------- Convenience commands ----------
\newcommand{\code}[1]{\texttt{\small #1}}
\newcommand{\term}[1]{\textit{#1}\index{#1}}
\newcommand{\apiendpoint}[1]{\texttt{\small\color{oreillyteal}#1}}

%% ---------- Epigraph styling ----------
\setlength{\epigraphwidth}{0.7\textwidth}
\epigraphfontsize{\small\itshape}

%% ---------- Figure caption styling ----------
\captionsetup{
  font={small,sf},
  labelfont={bf,color=oreillydark},
  format=hang,
  margin=1cm,
}

\endinput
