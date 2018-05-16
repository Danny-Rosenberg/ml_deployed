package main

import (
  //_"github.com/gorilla/mux"
  "fmt"
  "net/http"
  //"encoding/json"
  "encoding/xml"
  "reflect"
  _"io/ioutil"
  
)

type xmlResponse struct{
  Duplicate bool

}

type questions struct{
  QuestionOne string `xml:"one"`
  QuestionTwo string `xml:"two"`

}

func Homepage(w http.ResponseWriter, r *http.Request){
  fmt.Fprintf(w, "hello world!")

}

//This function is a test to receive POST data from 
//the frontend, and to understand the format
func questionResponse(w http.ResponseWriter, r *http.Request){
  fmt.Println("here is the type of the request body:")
  fmt.Println(reflect.TypeOf(r.Body)) 
  var t questions
  
  defer r.Body.Close()
  //receives requests in XML
  dec := xml.NewDecoder(r.Body)
  
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
  
  err := dec.Decode(&t)
  if err != nil {
    fmt.Println("error decoding into t:", err)

  } else {
    fmt.Println("here is decoded q1:", t.QuestionOne)
    fmt.Println("here is decoded q2:", t.QuestionTwo)

  }
   
    


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

