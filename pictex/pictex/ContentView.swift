//
//  ContentView.swift
//  pictex
//
//  Created by Len Huang on 8/18/20.
//  Copyright © 2020 PicTex Technologies. All rights reserved.
//

import SwiftUI
import Amplify
import AmplifyPlugins

struct ContentView: View {
    
    @State var isShowingImagePicker = false
    @State var imageInBox = UIImage()
    
    var body: some View {
        VStack {
            Image(uiImage: imageInBox).resizable().scaledToFill().frame(width:200,height:200).border(Color.black, width: 1).clipped()
            Button(action: {
                self.isShowingImagePicker.toggle()
            }, label: {
                Text("Select Image").font(.system(size: 32))
            }).sheet(isPresented: $isShowingImagePicker, content:{ ImagePickerView(isPresented: self.$isShowingImagePicker, selectedImage: self.$imageInBox)
            })
            Button(action: {
                uploadSelectedImage(image: self.imageInBox)
            }, label: {
                Text("Upload to S3").font(.system(size:32))
            })
                .padding(.top, 10.0)
        }
    }
}

struct ImagePickerView: UIViewControllerRepresentable {
    
    @Binding var isPresented: Bool
    @Binding var selectedImage: UIImage
    
    func makeUIViewController(context: UIViewControllerRepresentableContext<ImagePickerView>) -> UIViewController {
        let controller = UIImagePickerController()
        controller.delegate = context.coordinator
        return controller
    }
    
    func makeCoordinator() -> ImagePickerView.Coordinator {
        return Coordinator(parent: self)
    }
    
    // this is the tricky part
    class Coordinator: NSObject, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
        
        let parent: ImagePickerView
        init(parent: ImagePickerView){
            self.parent = parent
        }
        
        func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
            if let pickerImage = info[.originalImage] as? UIImage {
                self.parent.selectedImage = pickerImage
                print(pickerImage)
            }
            self.parent.isPresented = false
        }
    }
    
    func updateUIViewController(_ uiViewController: ImagePickerView.UIViewControllerType, context: UIViewControllerRepresentableContext<ImagePickerView>) {
    }
}

func uploadSelectedImage(image : UIImage) {
    guard let data = image.jpegData(compressionQuality: 0.75) else { return }
    let key = "images/" + NSUUID().uuidString + ".jpeg"
    Amplify.Storage.uploadData(key: key, data: data,
                               progressListener: { progress in
                                print("Progress: \(progress)")
    }, resultListener: { event in
        switch event {
        case .success(let data):
            print("Completed: \(data)")
        case .failure(let storageError):
            print("Failed: \(storageError.errorDescription). \(storageError.recoverySuggestion)")
        }
    })
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
