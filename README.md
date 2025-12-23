                           AUDIOBOOK GENERATOR
OBJECTIVE : 
            AudioBook Generator is a web application that allows users to upload text documents (PDF, DOCX) and automatically converts them into high-quality audiobooks.
EXECUTION PLAN : 
                                            User Uploads Documents
                                 
                                                   Text Extraction 

                                               LLM-Based Text Enrichment 

                                                  Text-to-Speech Conversion 

                                                      Audio Download
STEP 1 : Takes input from the user.
STEP 2 : Extracts text from the uploaded file. 
                PDF :- pdfplumber 
                DOCX :-  python-docx
                OUTPUT : Extracts text from the uploaded file.
STEP 3 : Enriches the extracted text 
               Used gemini-2.5-flash LLM model
               OUTPUT : Converts the text into listener friendly audiobook narration   style.
STEP 4 : Select the preferred language in the drop down.
               Used google translator for translating audio into preferred language.
STEP 5 : The enriched text converted into speech.
               gTTS is used for text-to speech conversion
               OUTPUT : 
                                • Generated can be listen itself or we can download lt.
                                • The downloaded file is in .mp3 format.


