//
//  CircleImage.swift
//  PicTeX
//
//  Created by Erica Chiang on 8/23/20.
//  Copyright © 2020 Erica Chiang. All rights reserved.
//

import SwiftUI

struct CircleImage: View {
    var body: some View {
        Image("cousins")
            .clipShape(Circle())
            .overlay(Circle().stroke(Color.white, lineWidth: 50))
            .scaleEffect(0.07)
            .shadow(radius: 20)
    }
}

struct CircleImage_Previews: PreviewProvider {
    static var previews: some View {
        CircleImage()
    }
}
