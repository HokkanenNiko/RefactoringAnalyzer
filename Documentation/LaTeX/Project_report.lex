
\documentclass[sigconf]{acmart}
\usepackage{geometry}
\geometry{a4paper, margin=1in}
\title{RefactoringAnalyzer Project Report}
\author{Niko Hokkanen, Carlos Pantin, Paavo Parviainen, Niko Siltala, Jack Sundholm}
\date{\today}
\usepackage{pdfpages}

\begin{document}

\maketitle

\section{Introduction}
This report is part of the coursework for the \textbf{Software Development, Maintenance, and Operations} course (811372A) in Fall 2024. The project involves mining refactoring activities from a set of software projects and analyzing the developer effort and bug-fixing commits associated with those refactorings.

The analysis uses several tools, including RefactoringMiner for identifying refactorings, and additional Python scripts to collect data on developer effort and issue tracking. This document provides an overview of the project, the data collected, and the methodology used.

\section{Repository Structure}
The project repository includes Python scripts and tools designed to perform the following tasks:

\begin{itemize}
  \item \texttt{DeveloperEffort.py}: Tracks the effort exerted by developers during the refactoring process by counting touched lines of code (TLOC).
  \item \texttt{DividedProjects.py}: Handles project division tasks, potentially for parallel analysis.
  \item \texttt{GetBugIssueData.py}: Collects issue tracking and bug-fixing commit information from GitHub's API.
  \item \texttt{RefactoringRunner.py}: Runs RefactoringMiner on each cloned repository to collect refactoring data.
  \item \texttt{ProduceUniqueRepos.py}: Gathers unique repositories for analysis from the dataset.
\end{itemize}

These files work together to produce the necessary output in the form of JSON, CSV, and other data formats as required by the coursework instructions.

\section{Methodology}
The methodology follows the project steps outlined in the coursework, including:

\subsection{Data Collection}
The dataset provided in the coursework is used to identify and clone the relevant GitHub repositories. Once cloned, RefactoringMiner is applied to analyze the refactoring history of each project. The CLI options of RefactoringMiner are used to mine all commits in each repository.

\subsection{Commit Differences}
For each refactoring commit (RC), the differences between the current commit and the previous commit are calculated. This data includes the modified lines of code (ADD, DEL) and the textual content of the diffs. Python's \texttt{pydriller} library is used for this analysis.

\subsection{Developer Effort}
Developer effort is measured by collecting the total number of touched lines of code (TLOC) for each refactoring. The \texttt{scc} tool is used to measure LOC in the refactoring commit and its predecessor.

\subsection{Bug-fixing Commits}
For projects using GitHub as an Issue Tracking System (ITS), the GitHub REST API is used to mine bug-fixing commits. The \texttt{GetBugIssueData.py} script collects the necessary issue data.

\section{Results}
The project produces several outputs, including:

\begin{itemize}
  \item Refactoring data in JSON format, with attributes such as refactoring type, commit hash, and inter-refactoring period.
  \item Commit diffs for each refactoring commit, including numerical data on the differences and the modified code content.
  \item Developer effort data, with attributes such as refactoring hash, previous hash, and TLOC.
  \item Bug-fixing commit data from GitHub's issue tracking system.
\end{itemize}

These results are compiled into a structured dataset, which forms the basis for the analysis performed in this report.


\section{Script and Requirement Mapping}
The following section maps the various Python scripts from the repository to the project requirements specified in the coursework instructions.

\subsection{Step (a) - Cloning GitHub Projects}
This step involves cloning the required repositories from GitHub. The \texttt{RefactoringRunner.py} script handles this task using the \texttt{subprocess} library to execute Git commands for cloning repositories from the list provided in \texttt{uniqueRepositories.txt}.

\subsection{Step (b) - Mining Refactoring Activity (RefactoringMiner)}
The \texttt{RefactoringRunner.py} script also runs RefactoringMiner to analyze the refactoring activity across all commits in each repository. It invokes the CLI commands for RefactoringMiner and produces the necessary output in JSON format for further analysis.

\subsection{Step (c) - Calculating Diff Changes}
This step is still pending implementation.

\subsection{Step (d) - Collecting Developer Effort (TLOC)}
The \texttt{DeveloperEffort.py} script handles the task of collecting the total touched lines of code (TLOC) for each refactoring. It uses the \texttt{scc} tool to gather LOC information from both the refactoring commit and the previous commit, and calculates the absolute difference.

\subsection{Step (e) - Mining Bug-Fixing Commits}
The \texttt{GetBugIssueData.py} script is responsible for collecting bug-fixing commits by interacting with GitHub's REST API. It queries GitHub's issue tracking system (ITS) to collect relevant issue data and stores the output for further analysis.

\subsection{Step (f) - Data Collection Logic and Submission Format}
The \texttt{Runner.py} script orchestrates the entire process, calling all relevant scripts and producing the required output files in JSON and CSV formats. This script is responsible for ensuring that each part of the process runs smoothly, from cloning repositories to generating refactoring data and developer effort statistics.

\section{Conclusion}
The \texttt{RefactoringAnalyzer} project mines and analyzes refactoring activities in software projects. By combining tools like RefactoringMiner and Python scripts, the project provides valuable insights into developer effort and bug-fixing activity, supporting the broader application of refactoring in practice.

\newpage
\appendix
\section{Repository List}
The following is the list of 381 Apache repositories used for the analysis in this project:

\begin{itemize}
  \item \url{https://github.com/apache/fineract}
  \item \url{https://github.com/apache/sling-org-apache-sling-feature-karaf}
  \item \url{https://github.com/apache/sling-org-apache-sling-committer-cli}
  \item \url{https://github.com/apache/hadoop-ozone}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-content-processing}
  \item \url{https://github.com/apache/sling-org-apache-sling-testing-osgi-mock}
  \item \url{https://github.com/apache/sling-org-apache-sling-feature-apiregions-model}
  \item \url{https://github.com/apache/sling-org-apache-sling-repoinit-it}
  \item \url{https://github.com/apache/sling-org-apache-sling-hc-support}
  \item \url{https://github.com/apache/sling-org-apache-sling-resourceresolver}
  \item \url{https://github.com/apache/sling-org-apache-sling-starter}
  \item \url{https://github.com/apache/sling-org-apache-sling-feature-apiregions}
  \item \url{https://github.com/apache/openmeetings}
  \item \url{https://github.com/apache/sling-org-apache-sling-engine}
  \item \url{https://github.com/apache/sling-org-apache-sling-distribution-journal-kafka}
  \item \url{https://github.com/apache/sling-org-apache-sling-repoinit-parser}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-cache-container-test}
  \item \url{https://github.com/apache/sling-org-apache-sling-api}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-sightly-repl}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-oak-server}
  \item \url{https://github.com/apache/sling-org-apache-sling-launchpad-startupmanager}
  \item \url{https://github.com/apache/submarine}
  \item \url{https://github.com/apache/sling-org-apache-sling-adapter}
  \item \url{https://github.com/apache/sling-org-apache-sling-extensions-webconsolesecurityprovider}
  \item \url{https://github.com/apache/sling-org-apache-sling-provisioning-model}
  \item \url{https://github.com/apache/sling-org-apache-sling-fsresource}
  \item \url{https://github.com/apache/jspwiki-builder}
  \item \url{https://github.com/apache/sling-org-apache-sling-contentparser-json}
  \item \url{https://github.com/apache/sling-org-apache-sling-i18n}
  \item \url{https://github.com/apache/sling-org-apache-sling-models-caconfig}
  \item \url{https://github.com/apache/sling-org-apache-sling-testing-resourceresolver-mock}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-java}
  \item \url{https://github.com/apache/plc4x}
  \item \url{https://github.com/apache/sling-org-apache-sling-servlets-post}
  \item \url{https://github.com/apache/sling-org-apache-sling-sitemap}
  \item \url{https://github.com/apache/poi-parent}
  \item \url{https://github.com/apache/sling-project-archetype}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-threads}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-jackrabbit-accessmanager}
  \item \url{https://github.com/apache/sling-org-apache-sling-xss}
  \item \url{https://github.com/apache/sling-org-apache-sling-testing-sling-mock}
  \item \url{https://github.com/apache/sling-org-apache-sling-feature-modelconverter}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-sightly}
  \item \url{https://github.com/apache/sling-org-apache-sling-resourceaccesssecurity}
  \item \url{https://github.com/apache/sling-kickstart-maven-plugin}
  \item \url{https://github.com/apache/sling-initial-content-archetype}
  \item \url{https://github.com/apache/sling-org-apache-sling-karaf-integration-tests}
  \item \url{https://github.com/apache/sling-org-apache-sling-security}
  \item \url{https://github.com/apache/commons-statistics}
  \item \url{https://github.com/apache/sling-scriptingbundle-maven-plugin}
  \item \url{https://github.com/apache/sling-org-apache-sling-distribution-journal-it}
  \item \url{https://github.com/apache/sling-org-apache-sling-feature-launcher}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-jsp-api}
  \item \url{https://github.com/apache/sling-org-apache-sling-servlets-get}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-jsp}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-freemarker}
  \item \url{https://github.com/apache/sling-org-apache-sling-starter-content}
  \item \url{https://github.com/apache/sling-org-apache-sling-resource-presence}
  \item \url{https://github.com/apache/sling-org-apache-sling-junit-teleporter}
  \item \url{https://github.com/apache/sling-org-apache-sling-karaf-configs}
  \item \url{https://github.com/apache/sling-content-package-archetype}
  \item \url{https://github.com/apache/sling-maven-plugin}
  \item \url{https://github.com/apache/sling-org-apache-sling-auth-core}
  \item \url{https://github.com/apache/incubator-hop}
  \item \url{https://github.com/apache/isis}
  \item \url{https://github.com/apache/sling-org-apache-sling-adapter-annotations}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-el-api}
  \item \url{https://github.com/apache/sling-org-apache-sling-contentparser-xml}
  \item \url{https://github.com/apache/cxf}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-sightly-testing-content}
  \item \url{https://github.com/apache/sling-org-apache-sling-rewriter}
  \item \url{https://github.com/apache/ofbiz-plugins}
  \item \url{https://github.com/apache/groovy}
  \item \url{https://github.com/apache/sling-feature-converter-maven-plugin}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-javascript}
  \item \url{https://github.com/apache/sling-org-apache-sling-installer-provider-file}
  \item \url{https://github.com/apache/sling-org-apache-sling-testing-clients}
  \item \url{https://github.com/apache/sling-org-apache-sling-nosql-launchpad}
  \item \url{https://github.com/apache/sling-org-apache-sling-feature}
  \item \url{https://github.com/apache/incubator-iotdb}
  \item \url{https://github.com/apache/sling-parent}
  \item \url{https://github.com/apache/sling-org-apache-sling-capabilities-jcr}
  \item \url{https://github.com/apache/commons-numbers}
  \item \url{https://github.com/apache/pdfbox-reactor}
  \item \url{https://github.com/apache/apache-dolphinscheduler}
  \item \url{https://github.com/apache/sling-org-apache-sling-testing-sling-mock-oak}
  \item \url{https://github.com/apache/struts}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-sightly-testing}
  \item \url{https://github.com/apache/sling-org-apache-sling-launchpad-test-fragment}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-jcr-file}
  \item \url{https://github.com/apache/sling-org-apache-sling-feature-extension-content}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-html}
  \item \url{https://github.com/apache/sling-whiteboard}
  \item \url{https://github.com/apache/sling-org-apache-sling-feature-applicationbuilder}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-mime}
  \item \url{https://github.com/apache/sling-org-apache-sling-servlets-resolver}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-thymeleaf}
  \item \url{https://github.com/apache/hop}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-sightly-compiler}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-messaging-mail}
  \item \url{https://github.com/apache/sling-org-apache-sling-nosql-couchbase-resourceprovider}
  \item \url{https://github.com/apache/sling-org-apache-sling-reqanalyzer}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-sightly-compiler-java}
  \item \url{https://github.com/apache/sling-org-apache-sling-feature-analyser}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-cache-api}
  \item \url{https://github.com/apache/sling-org-apache-sling-servlet-helpers}
  \item \url{https://github.com/apache/sling-org-apache-sling-caconfig-api}
  \item \url{https://github.com/apache/sling-org-apache-sling-connection-timeout-agent}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-scheduler}
  \item \url{https://github.com/apache/JMeter}
  \item \url{https://github.com/apache/sling-org-apache-sling-javax-activation}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-packageinit}
  \item \url{https://github.com/apache/sling-org-apache-sling-validation-test-services}
  \item \url{https://github.com/apache/sling-org-apache-sling-servlets-annotations}
  \item \url{https://github.com/apache/jackrabbit-filevault}
  \item \url{https://github.com/apache/sling-org-apache-sling-serviceusermapper}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-registration}
  \item \url{https://github.com/apache/sling-org-apache-sling-installer-core}
  \item \url{https://github.com/apache/sling-org-apache-sling-installer-it}
  \item \url{https://github.com/apache/sling-adapter-annotations}
  \item \url{https://github.com/apache/sling-org-apache-sling-auth-saml2}
  \item \url{https://github.com/apache/sling-org-apache-sling-event}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-groovy}
  \item \url{https://github.com/apache/sling-org-apache-sling-resourcemerger}
  \item \url{https://github.com/apache/sling-org-apache-sling-karaf-features}
  \item \url{https://github.com/apache/sling-org-apache-sling-testing-rules}
  \item \url{https://github.com/apache/sling-htl-maven-plugin}
  \item \url{https://github.com/apache/sling-org-apache-sling-feature-cpconverter}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-repoinit}
  \item \url{https://github.com/apache/sling-org-apache-sling-feature-inventoryprinter}
  \item \url{https://github.com/apache/sling-org-apache-sling-feature-extension-apiregions}
  \item \url{https://github.com/apache/sling-org-apache-sling-caconfig-integration-tests}
  \item \url{https://github.com/apache/sling-org-apache-sling-caconfig-bnd-plugin}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-johnzon}
  \item \url{https://github.com/apache/sling-org-apache-sling-models-api}
  \item \url{https://github.com/apache/sling-org-apache-sling-testing-hamcrest}
  \item \url{https://github.com/apache/sling-org-apache-sling-nosql-generic}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-messaging}
  \item \url{https://github.com/apache/sling-slingstart-maven-plugin}
  \item \url{https://github.com/apache/sling-org-apache-sling-testing-jcr-mock}
  \item \url{https://github.com/apache/sling-org-apache-sling-models-integration-tests}
  \item \url{https://github.com/apache/sling-org-apache-sling-junit-performance}
  \item \url{https://github.com/apache/sling-org-apache-sling-testing-caconfig-mock-plugin}
  \item \url{https://github.com/apache/sling-org-apache-sling-launchpad-integration-tests}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-osgi}
  \item \url{https://github.com/apache/apache-ratis}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-sightly-runtime}
  \item \url{https://github.com/apache/sling-org-apache-sling-feature-resolver}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-maintenance}
  \item \url{https://github.com/apache/sling-org-apache-sling-distribution-api}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-sightly-js-provider}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-core}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-jackrabbit-usermanager}
  \item \url{https://github.com/apache/sling-org-apache-sling-installer-provider-jcr}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-content-analyzing}
  \item \url{https://github.com/apache/sling-org-apache-sling-auth-form}
  \item \url{https://github.com/apache/apache-daffodil}
  \item \url{https://github.com/apache/commons-geometry}
  \item \url{https://github.com/apache/sling-org-apache-sling-startupfilter-disabler}
  \item \url{https://github.com/apache/commons-math}
  \item \url{https://github.com/apache/sling-org-apache-sling-junit-core}
  \item \url{https://github.com/apache/sling-org-apache-sling-thumbnails}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-webconsole}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-compiler}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-filetransfer}
  \item \url{https://github.com/apache/sling-org-apache-sling-installer-factory-feature}
  \item \url{https://github.com/apache/sling-org-apache-sling-tooling-support-install}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-spi}
  \item \url{https://github.com/apache/sling-org-apache-sling-discovery-oak}
  \item \url{https://github.com/apache/sling-org-apache-sling-contentparser-testutils}
  \item \url{https://github.com/apache/sling-org-apache-sling-testing-serversetup}
  \item \url{https://github.com/apache/sling-org-apache-sling-nosql-mongodb-resourceprovider}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-base}
  \item \url{https://github.com/apache/sling-org-apache-sling-junit-healthcheck}
  \item \url{https://github.com/apache/sling-org-apache-sling-capabilities}
  \item \url{https://github.com/apache/sling-org-apache-sling-testing-paxexam}
  \item \url{https://github.com/apache/sling-org-apache-sling-app-cms}
  \item \url{https://github.com/apache/sling-org-apache-sling-validation-examples}
  \item \url{https://github.com/apache/sling-org-apache-sling-auth-xing-oauth}
  \item \url{https://github.com/apache/sling-org-apache-sling-discovery-standalone}
  \item \url{https://github.com/apache/sling-org-apache-sling-models-impl}
  \item \url{https://github.com/apache/sling-archetype-parent}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-bundle-tracker-it}
  \item \url{https://github.com/apache/sling-org-apache-sling-junit-scriptable}
  \item \url{https://github.com/apache/sling-org-apache-sling-contentparser-api}
  \item \url{https://github.com/apache/sling-org-apache-sling-installer-factory-packages}
  \item \url{https://github.com/apache/sling-org-apache-sling-dynamic-include}
  \item \url{https://github.com/apache/camel}
  \item \url{https://github.com/apache/sling-org-apache-sling-feature-r2f}
  \item \url{https://github.com/apache/sling-jspc-maven-plugin}
  \item \url{https://github.com/apache/sling-org-apache-sling-installer-factory-configuration}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-crypto}
  \item \url{https://github.com/apache/sling-org-apache-sling-servlets-annotations-it}
  \item \url{https://github.com/apache/ofbiz-framework}
  \item \url{https://github.com/apache/sling-slingfeature-maven-plugin}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-esx}
  \item \url{https://github.com/apache/sling-org-apache-sling-validation-core}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-api}
  \item \url{https://github.com/apache/sling-org-apache-sling-contentparser-xml-jcr}
  \item \url{https://github.com/apache/sling-org-apache-sling-superimposing}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-metrics-rrd4j}
  \item \url{https://github.com/apache/sling-org-apache-sling-distribution-journal-messages}
  \item \url{https://github.com/apache/sling-org-apache-sling-pipes}
  \item \url{https://github.com/apache/sling-org-apache-sling-launchpad-base}
  \item \url{https://github.com/apache/sling-slingstart-archetype}
  \item \url{https://github.com/apache/sling-org-apache-sling-models-validation-impl}
  \item \url{https://github.com/apache/sling-org-apache-sling-installer-console}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-resource}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-metrics}
  \item \url{https://github.com/apache/gora}
  \item \url{https://github.com/apache/sling-org-apache-sling-karaf-distribution}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-resourcesecurity}
  \item \url{https://github.com/apache/sling-org-apache-sling-distribution-journal}
  \item \url{https://github.com/apache/sling-org-apache-sling-event-dea}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-classloader}
  \item \url{https://github.com/apache/sling-apache-sling-jar-resource-bundle}
  \item \url{https://github.com/apache/sling-org-apache-sling-bundleresource-impl}
  \item \url{https://github.com/apache/sling-org-apache-sling-testing-logging-mock}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-clam}
  \item \url{https://github.com/apache/sling-org-apache-sling-nosql-couchbase-client}
  \item \url{https://github.com/apache/sling-org-apache-sling-models-jacksonexporter}
  \item \url{https://github.com/apache/jackrabbit-filevault-package-maven-plugin}
  \item \url{https://github.com/apache/sling-org-apache-sling-graphql-core}
  \item \url{https://github.com/apache/sling-org-apache-sling-settings}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-jsp-jstl}
  \item \url{https://github.com/apache/org.apache.nemo:nemo-project}
  \item \url{https://github.com/apache/any23}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-contentloader}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-jsp-taglib}
  \item \url{https://github.com/apache/sling-launchpad-standalone-archetype}
  \item \url{https://github.com/apache/sling-feature-launcher-maven-plugin}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-jsp-taglib-compat}
  \item \url{https://github.com/apache/sling-org-apache-sling-installer-factory-model}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-log-webconsole}
  \item \url{https://github.com/apache/sling-org-apache-sling-karaf-launchpad-oak-tar-integration-tests}
  \item \url{https://github.com/apache/sling-org-apache-sling-feature-diff}
  \item \url{https://github.com/apache/sling-org-apache-sling-discovery-support}
  \item \url{https://github.com/apache/sling-org-apache-sling-testing-email}
  \item \url{https://github.com/apache/sling-org-apache-sling-clam}
  \item \url{https://github.com/apache/commons-rng}
  \item \url{https://github.com/apache/sling-org-apache-sling-launchpad-test-bundles}
  \item \url{https://github.com/apache/sling-org-apache-sling-validation-api}
  \item \url{https://github.com/apache/sling-org-apache-sling-fragment-ws}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-log}
  \item \url{https://github.com/apache/sling-org-apache-sling-jms}
  \item \url{https://github.com/apache/sling-launchpad-comparator}
  \item \url{https://github.com/apache/commons-math}
  \item \url{https://github.com/apache/sling-org-apache-sling-graphql-schema-aggregator}
  \item \url{https://github.com/apache/sling-org-apache-sling-distribution-sample}
  \item \url{https://github.com/apache/sling-org-apache-sling-resourceaccesssecurity-it}
  \item \url{https://github.com/apache/sling-org-apache-sling-serviceuser-webconsole}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-contentdetection}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-jcr-wrapper}
  \item \url{https://github.com/apache/incubator-tamaya}
  \item \url{https://github.com/apache/sling-org-apache-sling-installer-factory-subsystems-base}
  \item \url{https://github.com/apache/roller-master}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-bundle-tracker}
  \item \url{https://github.com/apache/sling-org-apache-sling-hapi-samplecontent}
  \item \url{https://github.com/apache/sling-org-apache-sling-caconfig-impl}
  \item \url{https://github.com/apache/sling-org-apache-sling-distribution-core}
  \item \url{https://github.com/apache/sling-org-apache-sling-extensions-logback-groovy-fragment}
  \item \url{https://github.com/apache/incubator-tamaya-extensions}
  \item \url{https://github.com/apache/sling-launchpad-debian}
  \item \url{https://github.com/apache/sling-org-apache-sling-feature-extension-unpack}
  \item \url{https://github.com/apache/sling-org-apache-sling-auth-xing-login}
  \item \url{https://github.com/apache/sling-org-apache-sling-resource-editor}
  \item \url{https://github.com/apache/sling-org-apache-sling-hc-it}
  \item \url{https://github.com/apache/sling-org-apache-sling-urlrewriter}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-jackrabbit-base}
  \item \url{https://github.com/apache/sling-org-apache-sling-discovery-commons}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-logservice}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-threaddump}
  \item \url{https://github.com/apache/sling-org-apache-sling-resourcecollection}
  \item \url{https://github.com/apache/karaf}
  \item \url{https://github.com/apache/sling-org-apache-sling-junit-remote}
  \item \url{https://github.com/apache/sling-org-apache-sling-feature-io}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-classloader}
  \item \url{https://github.com/apache/sling-org-apache-sling-jobs}
  \item \url{https://github.com/apache/incubator-ratis}
  \item \url{https://github.com/apache/sling-org-apache-sling-tooling-support-source}
  \item \url{https://github.com/apache/xmlbeans}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-js-nodetypes}
  \item \url{https://github.com/apache/sling-org-apache-sling-discovery-base}
  \item \url{https://github.com/apache/knox-gateway}
  \item \url{https://github.com/apache/sling-org-apache-sling-caconfig-spi}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-xproc}
  \item \url{https://github.com/apache/sling-org-apache-sling-launchpad-api}
  \item \url{https://github.com/apache/sling-org-apache-sling-jobs-it-services}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-webdav}
  \item \url{https://github.com/apache/sling-org-apache-sling-distribution-kryo-serializer}
  \item \url{https://github.com/apache/sling-org-apache-sling-event-api}
  \item \url{https://github.com/apache/sling-org-apache-sling-file-optimization}
  \item \url{https://github.com/apache/sling-org-apache-sling-mongodb}
  \item \url{https://github.com/apache/sling-org-apache-sling-jmx-provider}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-contentparser}
  \item \url{https://github.com/apache/sling-org-apache-sling-launchpad-test-services}
  \item \url{https://github.com/apache/sling-org-apache-sling-hc-samples}
  \item \url{https://github.com/apache/sling-org-apache-sling-installer-factory-deploymentpackage}
  \item \url{https://github.com/apache/sling-jcrinstall-bundle-archetype}
  \item \url{https://github.com/apache/sling-org-apache-sling-fragment-activation}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-davex}
  \item \url{https://github.com/apache/sling-org-apache-sling-distribution-avro-serializer}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-fsclassloader}
  \item \url{https://github.com/apache/sling-org-apache-sling-installer-hc}
  \item \url{https://github.com/apache/sling-org-apache-sling-bnd-models}
  \item \url{https://github.com/apache/sling-maven-launchpad-plugin}
  \item \url{https://github.com/apache/sling-servlet-archetype}
  \item \url{https://github.com/apache/sling-org-apache-sling-crankstart-test-model}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-cache-impl}
  \item \url{https://github.com/apache/sling-org-apache-sling-tracer}
  \item \url{https://github.com/apache/sling-org-apache-sling-hc-api}
  \item \url{https://github.com/apache/sling-org-apache-sling-extensions-classloader-leak-detector}
  \item \url{https://github.com/apache/sling-org-apache-sling-installer-provider-installhook}
  \item \url{https://github.com/apache/sling-org-apache-sling-query}
  \item \url{https://github.com/apache/sling-org-apache-sling-resourcebuilder}
  \item \url{https://github.com/apache/sling-launchpad-webapp-archetype}
  \item \url{https://github.com/apache/commons-compress}
  \item \url{https://github.com/apache/incubator-daffodil}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-api}
  \item \url{https://github.com/apache/sling-org-apache-sling-launchpad-testing}
  \item \url{https://github.com/apache/sling-org-apache-sling-launchpad-test-services-war}
  \item \url{https://github.com/apache/sling-org-apache-sling-launchpad-installer}
  \item \url{https://github.com/apache/sling-maven-jcrocm-plugin}
  \item \url{https://github.com/apache/sling-org-apache-sling-discovery-api}
  \item \url{https://github.com/apache/sling-org-apache-sling-oak-restrictions}
  \item \url{https://github.com/apache/sling-org-apache-sling-auth-xing-api}
  \item \url{https://github.com/apache/sling-bundle-archetype}
  \item \url{https://github.com/apache/sling-org-apache-sling-bnd-plugins}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-sightly-models-provider}
  \item \url{https://github.com/apache/ant-master}
  \item \url{https://github.com/apache/sling-org-apache-sling-fragment-xml}
  \item \url{https://github.com/apache/sling-org-apache-sling-extensions-webconsolebranding}
  \item \url{https://github.com/apache/sling-org-apache-sling-resource-inventory}
  \item \url{https://github.com/apache/sling-org-apache-sling-commons-testing}
  \item \url{https://github.com/apache/sling-org-apache-sling-tenant}
  \item \url{https://github.com/apache/sling-org-apache-sling-mom}
  \item \url{https://github.com/apache/sling-org-apache-sling-discovery-impl}
  \item \url{https://github.com/apache/sling-org-apache-sling-resource-filter}
  \item \url{https://github.com/apache/sling-org-apache-sling-hapi}
  \item \url{https://github.com/apache/sling-org-apache-sling-scripting-console}
  \item \url{https://github.com/apache/sling-org-apache-sling-hapi-client}
  \item \url{https://github.com/apache/sling-org-apache-sling-jcr-repository-it-resource-versioning}
  \item \url{https://github.com/apache/sling-org-apache-sling-tail}
  \item \url{https://github.com/apache/sling-org-apache-sling-fragment-nashorn}
  \item \url{https://github.com/apache/sling-taglib-archetype}
  \item \url{https://github.com/apache/sling-site}
  \item \url{https://github.com/apache/sling-org-apache-sling-extensions-slf4j-mdc}
  \item \url{https://github.com/apache/sling-org-apache-sling-servlets-resolver-api}
  \item \url{https://github.com/apache/sling-org-apache-sling-datasource}
  \item \url{https://github.com/apache/sling-org-apache-sling-bnd-plugin-headers-parameters-remove}
  \item \url{https://github.com/apache/sling-org-apache-sling-installer-factory-subsystems}
  \item \url{https://github.com/apache/sling-org-apache-sling-fragment-transaction}
  \item \url{https://github.com/apache/sling-org-apache-sling-featureflags}
  \item \url{https://github.com/apache/shiro}
  \item \url{https://github.com/apache/sling-org-apache-sling-jobs-it}
  \item \url{https://github.com/apache/sling-org-apache-sling-crankstart-test-services}
  \item \url{https://github.com/apache/sling-org-apache-sling-startupfilter}
  \item \url{https://github.com/apache/sling-org-apache-sling-kickstart}
  \item \url{https://github.com/apache/sling-org-apache-sling-hc-junit-bridge}
  \item \url{https://github.com/apache/incubator-milagro-MPC}
  \item \url{https://github.com/apache/sling-org-apache-sling-paxexam-util}
  \item \url{https://github.com/apache/fineract-cn-group-finance}
  \item \url{https://github.com/apache/milagro}
  \item \url{https://github.com/apache/sling-org-apache-sling-distribution-it}
  \item \url{https://github.com/apache/sling-org-apache-sling-starter-startup}
  \item \url{https://github.com/apache/log4cxx}
  \item \url{https://github.com/apache/incubator-seatunnel}
  \item \url{https://github.com/apache/incubator-tamaya-sandbox}
  \item \url{https://github.com/apache/servicecomb-toolkit}
  \item \url{https://github.com/apache/servicecomb-pack}
  \item \url{https://github.com/apache/jspwiki}
  \item \url{https://github.com/apache/poi}
  \item \url{https://github.com/apache/pdfbox-jbig2}
  \item \url{https://github.com/apache/dolphinscheduler}
  \item \url{https://github.com/apache/ratis}
  \item \url{https://github.com/apache/daffodil}
  \item \url{https://github.com/apache/incubator-nemo}
  \item \url{https://github.com/apache/roller}
  \item \url{https://github.com/apache/knox}
  \item \url{https://github.com/apache/ant}
  \item \url{https://github.com/apache/logging-log4cxx}

\end{itemize}
\newpage
\appendix
\section{Project Instructions}
Project instructions are included in the appendix on the next page.

\includepdf[pages=-]{PROJECT_OPTION_2__SDMO.pdf}
\end{document}
