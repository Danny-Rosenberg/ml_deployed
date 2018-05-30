package main

import (
  //_"github.com/gorilla/mux"
  "fmt"
  "net/http"
  //"encoding/json"
  "encoding/xml"
  _"reflect"
  _"io/ioutil"
  "os/exec"
  
)

type xmlResponse struct{
  Duplicate bool

}

type questions struct{
  QuestionOne string `xml:"one"`
  QuestionTwo string `xml:"two"`
  isDuplicate int `xml:"is_duplicate"`

}

func insert(qs questions){
  cmd := exec.Command("insert.py", "qs.one", "qs.two", "qs.isDuplicate" )
  cmd.Start()

}


func Homepage(w http.ResponseWriter, r *http.Request){
  fmt.Fprintf(w, "hello world!")

}


//This function is a test to receive POST data from 
//the frontend, and to understand the format
func questionResponse(w http.ResponseWriter, r *http.Request){
  fmt.Println("inside questionResponse")
  var t questions
  
  defer r.Body.Close()
  //receives requests in XML
  dec := xml.NewDecoder(r.Body)
  
  err := dec.Decode(&t)
  if err != nil {
    fmt.Println("error decoding into t:", err)

  } else {
    fmt.Println("here is decoded q1:", t.QuestionOne)
    fmt.Println("here is decoded q2:", t.QuestionTwo)
    fmt.Println("here is decoded isDuplicate:", t.isDuplicate)
  }
  
  //we'll get a response from the model
  
  response := true
  
  resp := &xmlResponse{Duplicate : response}
  w.WriteHeader(200)
  w.Header().Set("Cache-Control", "max-age=0") 
  
  data, err := xml.Marshal(resp)
  w.Write(data)
   
  
  //used to extract raw bytes and convert into strings, no formatting
  /*
  body, err := ioutil.ReadAll(r.Body)
  if err != nil{
    fmt.Println("error reading http body:", err)
    
  } else {
    fmt.Println("here is the body!", body)
    size := len(body)
    s := string(body[:size])
    fmt.Println(s) 
  } 
  */


}


func main(){
  
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

