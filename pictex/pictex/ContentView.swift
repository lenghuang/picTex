//
//  ContentView.swift
//  pictex
//
//  Created by Len Huang on 8/18/20.
//  Copyright © 2020 PicTex Technologies. All rights reserved.
//

import SwiftUI
import UIKit
import Amplify
import AmplifyPlugins

struct ContentView: View {
    
    @State var isShowingImagePicker = false
    @State var imageInBox = UIImage()
    @State var uploadLoading = false
    @State var uploadSuccess = ""
    @State var key = ""
    
    var cflink = "https://d37crjhbub9zgu.cloudfront.net/public/"
    
    var body: some View {
        LoadingView(isShowing: self.$uploadLoading) {
            self.vertical
        }
    }
    
    var vertical : some View {
        VStack {
            Spacer()
            Text("PicTex: \nUpload an Image")
                .font(.largeTitle)
                .fontWeight(.semibold)
                .multilineTextAlignment(.center)
            //            Image(uiImage: imageInBox).resizable().aspectRatio(contentMode: .fit).frame(width:375,height:450).border(Color.black, width: 1).clipped()
            GeometryReader { geo in
                VStack{
                    Image(uiImage: self.imageInBox)
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                        .frame(width: geo.size.width * 0.9, height: geo.size.height * 0.9).border(Color.blue, width: 1)
                    Button(action: {
                        self.isShowingImagePicker.toggle()
                    }, label: {
                        Text("Select Image")
                    }).sheet(isPresented: self.$isShowingImagePicker, content:{ ImagePickerView(isPresented: self.$isShowingImagePicker, selectedImage: self.$imageInBox)
                    })
                }
            }
            Button(action: {
                self.uploadSelectedImage(image: self.imageInBox)
            }, label: {
                Text("Upload to S3").foregroundColor(Color.white)
            })
                .padding().font(.system(size: 20))
                .background(/*@START_MENU_TOKEN@*/Color.blue/*@END_MENU_TOKEN@*/).cornerRadius(50)
            Button(self.uploadSuccess == "" ? "" : "Cick here to download") {UIApplication.shared.open(URL(string: self.cflink + self.key)!)}
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
        
        let key = NSUUID().uuidString + ".jpeg"
        self.key = key
        
        guard let data = image.jpegData(compressionQuality: 0.75) else { return }
        
        Amplify.Storage.uploadData(key: key, data: data,
                                   progressListener: { progress in
                                    print("Progress: \(progress)")
        }, resultListener: { event in
            switch event {
            case .success(let data):
                print("Completed: \(data)")
                self.uploadSuccess = "Upload success!"
            case .failure(let storageError):
                print("Failed: \(storageError.errorDescription). \(storageError.recoverySuggestion)")
                self.uploadSuccess = "Uh oh there's been an error: " + storageError.errorDescription
            }
            self.uploadLoading.toggle()
        })
    }
    
}


struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
