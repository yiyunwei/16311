% 16-311 Homework 1 Framework
% Written by Humphrey Hu 1/16/2014
% humhu@cmu.edu
% Hannah

% Please type your first and last name here
% Please type your Andrew ID here

function [] = waldo(searchImage)

% This function finds Waldos in an image
%   Input: searchImage in .png format
%   Output: output.txt with coordinates in x y\n form
%   This function should be run with the sample waldo
%   (wald.png) in the same directory

%% 1. Image Basics

waldoImage = imread('waldo.png');
sceneImage = imread(searchImage);

%% 2. Find Waldo

% FILL IN YOUR CODE HERE TO FIND THE WALDOS
waldo2 = waldoImage;
for i=1:size(waldo2, 1)
    for j=1:size(waldo2, 2)
        if(waldo2(i, j, 1) < 175)
            waldo2(i, j,:) = 0;
        else
            waldo2(i, j,:) = 255;
        end
    end
end
imwrite(waldo2, 'waldo2.png');
temp = waldo2(:,:,1);
for i=1:size(waldo2, 1)
    for j=1:size(waldo2, 2)
        if(temp(i, j) < 175)
            temp(i, j) = 1;
        else
            temp(i, j) = 0;
        end
    end
end

waldoBig = zeros(size(waldo2, 1)*2);
for i=1:size(waldo2, 1)
    for j=1:size(waldo2, 2)
        x = 1+(i-1)*2;
        y = 1+(j-1)*2;
        waldoBig(x:x+1, y:y+1) = waldo2(i, j, 1);
    end
end
imwrite(waldoBig, 'waldobig.png');

newscene = sceneImage(:,:,1);
for i=1:size(newscene, 1)
    for j=1:size(newscene, 2)
        if(newscene(i, j) < 175)
            newscene(i,j) = 1;
        else
            %newscene(i,j,:) = 255;
            newscene(i,j) = 0;
        end
    end
end
%imwrite(newscene, 'newscene.png');

final = zeros(16,2);

ind = 1;
for i=1:size(newscene, 1)-size(waldo2, 1)
    for j=1:size(newscene, 2)-size(waldo2, 2)
        count = 0;
        for m=i:i+size(waldo2, 1)-1
            for n=j:j+size(waldo2, 2)-1
                if (newscene(m,n) == temp(m-i+1, n-j+1))
                    count = count + 1;
                end
            end
        end
        if(count > 37)
            final(ind, :) = [j+3 i+3];
            ind = ind + 1;
        end
    end
end

%% 3. Write the output.txt file

% First we open a file and get a file ID # with fopen(). 'w' specifies we
% want to write.
file_id = fopen('output.txt', 'w');
if file_id == -1    % -1 is an invalid file ID and signals failure
    fprintf('File creation failed!\n');
    return;
end

% Now we can write to the file using fprintf (formatted print to file)
% fprintf uses a format specifier string, where %d represents an integer
% and %f represents a floating point number. You can then give fprintf the
% value you want to substitute into the string as additional arguments.
%'\n' is the special character for newline (or the enter key), and '/t'
% is the tab character. If the file ID is given to fprintf, it will write
% into the file instead of the terminal.

% FILL IN YOUR CODE HERE TO WRITE TO THE OUTPUT.TXT FILE
for i=1:16
    fprintf(file_id, "%d %d\n", final(i, 1), final(i, 2));
end

% Finally when you're done, you should close the file with fclose()
fclose(file_id);

end