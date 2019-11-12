% U-Hack 2019

clc;clear;close all;
count = 0;
cc = 0;
cmap = colormap("autumn");

videoplayer = vision.VideoPlayer;
% video file read
v = VideoReader('Balloon_Gad_1.mov');
v_write = VideoWriter('gadVis60_text.avi');
v_write.FrameRate = 59.75;
position =  [1 50];
box_color = 'green';
open(v_write)
while hasFrame(v)
    frame = readFrame(v);
    I = uint8(rgb2gray(frame));
    rect = [326.5100  375.5100  464.9800  352.980];
    j = imcrop(I,rect);
    zero_frame = zeros(size(I,1),size(I,2));
    zero_frame(round(rect(2)):round(rect(2))+round(rect(4))-1, round(rect(1)):round(rect(1))+round(rect(3))-1)= j;
    %zero_frame = mat2gray(zero_frame);
    temp = zero_frame;
    temp(temp<200) = 0;
    temp(temp>=200)=1;
    Ib = temp;
    % Thresholding
    %level = graythresh(I)+0.1;
    %Ib = imbinarize(zero_frame,0.85);
    
    %removal of small objects
    P = 500;
    Ib1 = bwareaopen(Ib,P);
    
    % %removal of large objects
    Ib3 = Ib1-bwareaopen(Ib1, 2500);
    Ib3 = logical(Ib3);
    st = regionprops(Ib3,'BoundingBox');
    %finding brightest objects
    if ~isempty(st)
        count = count+1;
        if length(st)>1
            Conn_comp = bwconncomp(Ib3);
            for i =1: Conn_comp.NumObjects
                Ids_list= Conn_comp.PixelIdxList;
                mean_comp(i) = mean(I(Ids_list{i}));
            end
            %mean_comp = cell2mat(mean_comp);
            [MM,Ind_bb]=max(mean_comp);
            
            bbox = st(Ind_bb).BoundingBox;
            clear mean_comp
        else
            bbox = st(1).BoundingBox;
        end
        
        clear Ind_bb
        
        rgbImage = cat(3, I, I, I);
        blob = ind2rgb(Ib3, cmap);
        
        
        %     imshow(Ib3,[]);
        %     pause(0.0003);
        
        C1 = imoverlay(rgbImage,Ib3,'red');
        C2 = insertShape(C1,"Rectangle",bbox,'LineWidth',3,'Color',"green");
        %imshowpair(I,Ib3,'blend'); pause(0.000001);
        Gw = montage({rgbImage,C2});
        frame_write = Gw.CData;
        duration = count./59.75;
        text_duration= ['Visibility Duration: ' num2str(duration,'%0.2f') 'Seconds'];
        frame_final = insertText(frame_write,position,['Visibility Duration: ' num2str(duration,'%0.2f') 'Seconds'],'FontSize',26,'BoxColor',...
            box_color,'BoxOpacity',0.4,'TextColor','white');
    else
        rgbImage = cat(3, I, I, I);
        Gw = montage({rgbImage,rgbImage});
        frame_write = Gw.CData;
        duration = count./59.75;
        text_duration= ['Visibility Duration: ' num2str(duration,'%0.2f') 'Seconds'];
        frame_final = insertText(frame_write,position,['Visibility Duration: ' num2str(duration,'%0.2f') 'Seconds'],'FontSize',26,'BoxColor',...
            box_color,'BoxOpacity',0.4,'TextColor','white');
        
    end
    %mont = cat(3,rgbImage,C2);
    
    videoplayer(frame_final)
    writeVideo(v_write,frame_final);
    
end
close(v_write)

