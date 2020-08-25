//
//  ScanView.swift
//  PicTeX
//
//  Created by Erica Chiang on 8/23/20.
//  Copyright © 2020 Erica Chiang. All rights reserved.
//

import SwiftUI
import UIKit
import Amplify
import AmplifyPlugins

struct ScanView: View {
    
    @State var isShowingImagePicker = false
    @State var camera = false
    @State var imageInBox = UIImage()
    @State var uploadLoading = false
    @State var uploadSuccess = ""
    @State var key = ""
    
    var body: some View {
        ZStack{
            if uploadSuccess == "yay" {
                DownloadView(key: self.$key)
            } else {
                LoadingView(isShowing: self.$uploadLoading) {
                    self.vertical
                }
            }
        }
    }
    
    var vertical : some View {
        VStack {
            Spacer()
            Text("Upload an image or scan a new image!")
                .font(.largeTitle)
                .fontWeight(.semibold)
                .multilineTextAlignment(.center)
            Image(uiImage: imageInBox).resizable().frame(width:375,height:450).aspectRatio(contentMode: .fill).border(Color.green, width: 1).clipped()
            
            Text("Select Image With").foregroundColor(Color.green)
            HStack {
                Button(action: {
                    self.isShowingImagePicker.toggle()
                    self.camera = true
                }, label: {
                    Image(systemName: "camera")
                    Text("Camera")
                }).sheet(isPresented: self.$isShowingImagePicker, content:{ ImagePickerView(isPresented: self.$isShowingImagePicker, selectedImage: self.$imageInBox, camera: self.$camera)
                })
                Button(action: {
                    self.isShowingImagePicker.toggle()
                    self.camera = false
                }, label: {
                    Image(systemName: "photo")
                    Text("Photo Gallery")
                }).sheet(isPresented: self.$isShowingImagePicker, content:{ ImagePickerView(isPresented: self.$isShowingImagePicker, selectedImage: self.$imageInBox, camera: self.$camera)
                })
            }.foregroundColor(Color.green)
            Spacer()
            Button(action: {
                self.uploadSelectedImage(image: self.imageInBox)
            }, label: {
                Text("Upload to S3").foregroundColor(Color.white)
            })
                .padding().font(.system(size: 20))
                .background(Color.green).cornerRadius(50)
            Text(self.uploadSuccess != "" || self.uploadSuccess != "yay" ? "" : self.uploadSuccess)
            Button(action: {
                self.imageInBox = UIImage()
                self.uploadSuccess = ""
                self.key = ""
            }, label: {
                Text("Reset").foregroundColor(Color.red)
            })
            Spacer()
        }
        
    }
    
    func uploadSelectedImage(image : UIImage) {
        self.uploadLoading.toggle()
        self.uploadSuccess = ""
        
        let key = "picture/" + NSUUID().uuidString + ".jpeg"
        let cflink = "https://d37crjhbub9zgu.cloudfront.net/public/"
        
        guard let data = image.jpegData(compressionQuality: 0.75) else { return }
        
        Amplify.Storage.uploadData(key: key, data: data,
                                   progressListener: { progress in
                                    print("Progress: \(progress)")
        }, resultListener: { event in
            switch event {
            case .success(let data):
                print("Completed: \(data)")
                self.lambdaHandler(cflink: cflink + key)
            case .failure(let storageError):
                print("Failed: \(storageError.errorDescription). \(storageError.recoverySuggestion)")
                self.uploadSuccess = "Uh oh there's been an error: " + storageError.errorDescription
                self.uploadLoading.toggle()
            }
        })
    }
    
    struct Response: Codable {
        var statusCode : Int
        var key : String
        var body : String
    }
    
    func lambdaHandler(cflink : String) {
        let lambda = "https://xo2hfza854.execute-api.us-east-1.amazonaws.com/prod/upload-to-s3?file="
        print(lambda + cflink)
        let url = URL(string: lambda + cflink)!
        let task = URLSession.shared.dataTask(with: url) {(data, response, error) in
            if let data = data {
                if let decodedResponse = try? JSONDecoder().decode(Response.self, from: data) {
                    // we have good data – go back to the main thread
                    DispatchQueue.main.async {
                        // update the key of the tex file
                        self.key = decodedResponse.key
                    }
                    self.uploadSuccess = "yay"
                    self.uploadLoading.toggle()
                    // everything is good, so we can exit
                    return
                }
            }
            // if we're still here it means there was a problem
            print("Fetch failed: \(error?.localizedDescription ?? "Unknown error")")
        }
        task.resume()
    }
}

struct ScanView_Previews: PreviewProvider {
    static var previews: some View {
        ScanView()
    }
}
