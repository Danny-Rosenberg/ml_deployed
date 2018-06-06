package main

import (
  //_"github.com/gorilla/mux"
  "fmt"
  "net/http"
  //"encoding/json"
  "encoding/xml"
  "os/exec"
  "os"
  "bytes"
  
)

type xmlResponse struct{
  Duplicate bool

}

type questions struct{
  QuestionOne string `xml:"one"`
  QuestionTwo string `xml:"two"`
  Duplicate string `xml:"is_dup"`

}

//inserts a set of labeled questions into the sqlite database
func insert(qs questions){
  cmd := exec.Command("./wrapper.sh", qs.QuestionOne, qs.QuestionTwo, qs.Duplicate)
  cmdOutput := &bytes.Buffer{}
  cmd.Stdout = cmdOutput
  err := cmd.Run()
  if err != nil {
    os.Stderr.WriteString(err.Error())
  }
  fmt.Print(string(cmdOutput.Bytes()))

}


func Homepage(w http.ResponseWriter, r *http.Request){
  fmt.Fprintf(w, "hello world!")

}


//trains model, could happen everytime the server starts or 
//after a certain of labeled instances enter the db
func trainModel(){
  


}


//This function is a test to receive POST data from 
//the frontend, and to understand the format
func questionResponse(w http.ResponseWriter, r *http.Request){
  var t questions
  
  defer r.Body.Close()
  //receives requests in XML
  dec := xml.NewDecoder(r.Body)
  
  err := dec.Decode(&t)
  if err != nil {
    fmt.Println("error decoding into t:", err)

  } else {
    fmt.Println("here is t:", t)
    fmt.Println("here is decoded q1:", t.QuestionOne)
    fmt.Println("here is decoded q2:", t.QuestionTwo)
    fmt.Println("here is decoded Duplicate:", t.Duplicate)
  }
  
  //insert into db
  insert(t)
  
  //we'll get a response from the model
  
  response := true
  
  resp := &xmlResponse{Duplicate : response}
  w.WriteHeader(200)
  w.Header().Set("Cache-Control", "max-age=0") 
  
  data, err := xml.Marshal(resp)
  w.Write(data)

}

func main(){
    
    /*
  cmd := exec.Command("./test.py")
  if err:= cmd.Run(); err != nil{
    fmt.Println("error: ", err)
  }
  */
  
  fs := http.FileServer(http.Dir("./static"))
  
  http.Handle("/", fs) 
  http.HandleFunc("/data", questionResponse)

/*
  srv := &http.Server{
    Addr: "127.0.0.1:8080",
    WriteTimeout: 15 * time.Second,
    ReadTimeout:  15 * time.Second,

  }
*/
  //fmt.Println(srv.ListenAndServe()) 
  fmt.Println(http.ListenAndServe(":8080", nil))  

}

