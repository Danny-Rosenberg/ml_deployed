package main

import (
  //_"github.com/gorilla/mux"
  "fmt"
  "net/http"
 _"time"
)

func Homepage(w http.ResponseWriter, r *http.Request){
  fmt.Fprintf(w, "hello world!")

}


func main(){

  //r := mux.NewRouter()

  //r.Host("http://localhost")
  //r.HandleFunc("/", Homepage)
  
  fs := http.FileServer(http.Dir("./static"))
  //http.Handle("/static", http.StripPrefix("/static/",fs)) 
  
  http.Handle("/", fs) 
  //r.PathPrefix("/static/").Handler(http.StripPrefix("/static/", http.FileServer(http.Dir("."))))

/*
  srv := &http.Server{
    Handler: r,
    Addr: "127.0.0.1:8080",
    WriteTimeout: 15 * time.Second,
    ReadTimeout:  15 * time.Second,

  }
*/
  //http.Handle("/", r) 
  //fmt.Println(srv.ListenAndServe()) 
  fmt.Println(http.ListenAndServe(":8080", nil))  

}

